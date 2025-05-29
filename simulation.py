import mesa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from enum import Enum

class GossipState(Enum):
    """Status agen dalam penyebaran gosip"""
    IGNORANT = 0    # Belum tahu gosip (biru)
    SPREADER = 1    # Menyebarkan gosip (merah)
    STIFLER = 2     # Sudah bosan gosip (hijau)
    RESISTANT = 3   # Kebal gosip (abu-abu)

class PersonAgent(mesa.Agent):
    """Agen individu dalam simulasi penyebaran gosip"""
    
    def __init__(self, unique_id, model, is_resistant=False):
        super().__init__(unique_id, model)
        self.state = GossipState.RESISTANT if is_resistant else GossipState.IGNORANT
        self.days_spreading = 0
        self.max_spread_days = np.random.randint(2, 6)  # 2-5 hari menyebar
        self.social_connections = []  # Koneksi sosial global
        self.communication_probability = np.random.uniform(0.1, 0.4)  # Seberapa sering berkomunikasi
        
    def create_social_connections(self):
        """Membuat koneksi sosial dengan agen lain (teman, keluarga, kolega)"""
        all_agents = list(self.model.schedule.agents)
        all_agents.remove(self)  # Hapus diri sendiri
        
        # Setiap agen memiliki 3-15 koneksi sosial
        num_connections = np.random.randint(3, 16)
        self.social_connections = self.random.sample(all_agents, 
                                                   min(num_connections, len(all_agents)))
        
    def step(self):
        """Langkah eksekusi agen setiap iterasi"""
        if self.state == GossipState.SPREADER:
            self.spread_gossip_local()      # Sebarkan ke tetangga
            self.spread_gossip_global()     # Sebarkan melalui koneksi sosial
            self.days_spreading += 1
            
            # Berhenti menyebar setelah beberapa hari
            if self.days_spreading >= self.max_spread_days:
                self.state = GossipState.STIFLER
                
        elif self.state == GossipState.IGNORANT:
            self.listen_for_gossip_local()   # Dengar dari tetangga
            self.listen_for_gossip_global()  # Dengar dari koneksi sosial
    
    def spread_gossip_local(self):
        """Menyebarkan gosip ke tetangga fisik"""
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=1
        )
        
        for neighbor in neighbors:
            if neighbor.state == GossipState.IGNORANT:
                if self.random.random() < self.model.spread_probability:
                    neighbor.hear_gossip()
    
    def spread_gossip_global(self):
        """Menyebarkan gosip melalui koneksi sosial (telepon, media sosial, dll)"""
        for connection in self.social_connections:
            if connection.state == GossipState.IGNORANT:
                # Peluang komunikasi dengan koneksi sosial
                if self.random.random() < self.communication_probability:
                    # Peluang menyebarkan gosip dalam komunikasi
                    if self.random.random() < self.model.global_spread_probability:
                        connection.hear_gossip()
    
    def hear_gossip(self):
        """Mendengar gosip dan mungkin mulai menyebar"""
        if self.state == GossipState.IGNORANT:
            if self.random.random() < self.model.believe_probability:
                self.state = GossipState.SPREADER
                self.days_spreading = 0
    
    def listen_for_gossip_local(self):
        """Mendengarkan gosip secara pasif dari tetangga fisik"""
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=1
        )
        
        spreader_neighbors = [n for n in neighbors if n.state == GossipState.SPREADER]
        
        if spreader_neighbors:
            # Semakin banyak spreader, semakin mudah mendengar
            hearing_chance = min(0.8, len(spreader_neighbors) * 0.2)
            if self.random.random() < hearing_chance:
                self.hear_gossip()
    
    def listen_for_gossip_global(self):
        """Mendengarkan gosip dari koneksi sosial"""
        spreader_connections = [c for c in self.social_connections 
                              if c.state == GossipState.SPREADER]
        
        for connection in spreader_connections:
            # Peluang menerima komunikasi dari koneksi yang menyebar gosip
            if self.random.random() < connection.communication_probability:
                # Peluang mendengar gosip dalam komunikasi
                if self.random.random() < self.model.global_spread_probability:
                    self.hear_gossip()
                    break  # Cukup dengar sekali per step

class GossipModel(mesa.Model):
    """Model simulasi penyebaran gosip"""
    
    def __init__(self, width=30, height=30, spread_probability=0.3, 
                 believe_probability=0.6, resistance_rate=0.15, 
                 initial_spreaders=3, global_spread_probability=0.15):
        super().__init__()
        
        # Parameter model
        self.width = width
        self.height = height
        self.spread_probability = spread_probability
        self.believe_probability = believe_probability
        self.resistance_rate = resistance_rate
        self.initial_spreaders = initial_spreaders
        self.global_spread_probability = global_spread_probability  # Peluang penyebaran global
        
        # Grid dan scheduler
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        self.schedule = mesa.time.RandomActivation(self)
        self.step_count = 0  # Tambahkan counter step
        
        # Data collector
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Ignorant": lambda m: sum(1 for a in m.schedule.agents 
                                        if a.state == GossipState.IGNORANT),
                "Spreader": lambda m: sum(1 for a in m.schedule.agents 
                                        if a.state == GossipState.SPREADER),
                "Stifler": lambda m: sum(1 for a in m.schedule.agents 
                                       if a.state == GossipState.STIFLER),
                "Resistant": lambda m: sum(1 for a in m.schedule.agents 
                                         if a.state == GossipState.RESISTANT)
            }
        )
        
        # Buat agen
        self.create_agents()
        
        # Buat koneksi sosial setelah semua agen dibuat
        self.create_social_network()
        
        # Collect data awal (hari ke-0)
        self.datacollector.collect(self)
        self.running = True
    
    def create_agents(self):
        """Membuat dan menempatkan agen di grid"""
        agent_id = 0
        
        # Buat semua agen
        for x in range(self.width):
            for y in range(self.height):
                # Tentukan apakah agen resistant
                is_resistant = self.random.random() < self.resistance_rate
                
                agent = PersonAgent(agent_id, self, is_resistant)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
                agent_id += 1
        
        # Set beberapa agen sebagai spreader awal
        non_resistant = [a for a in self.schedule.agents if not a.state == GossipState.RESISTANT]
        initial_spreaders = self.random.sample(non_resistant, 
                                             min(self.initial_spreaders, len(non_resistant)))
        
        for agent in initial_spreaders:
            agent.state = GossipState.SPREADER
    
    def create_social_network(self):
        """Membuat jaringan sosial untuk semua agen"""
        for agent in self.schedule.agents:
            if agent.state != GossipState.RESISTANT:  # Resistant agents have fewer connections
                agent.create_social_connections()
    
    def step(self):
        """Satu langkah simulasi"""
        self.step_count += 1
        self.schedule.step()
        self.datacollector.collect(self)
        
        # Stop jika tidak ada spreader
        spreader_count = sum(1 for a in self.schedule.agents 
                           if a.state == GossipState.SPREADER)
        if spreader_count == 0:
            self.running = False

class EnhancedGossipVisualization:
    """Visualisasi yang ditingkatkan untuk simulasi"""
    
    def __init__(self, model, max_steps=50):
        self.model = model
        self.max_steps = max_steps
        
        # Warna untuk setiap state
        colors = ['#87CEEB', '#FF6B6B', '#98FB98', '#D3D3D3']  # Biru, Merah, Hijau, Abu
        self.cmap = ListedColormap(colors)
        
        # Setup figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(16, 7))
        self.fig.suptitle('Simulasi Penyebaran Gosip dengan Interaksi Global', 
                         fontsize=16, fontweight='bold')
        
        # Grid visualization
        self.mat = self.ax1.imshow(self.get_grid_state(), cmap=self.cmap, 
                                  vmin=0, vmax=3, interpolation='nearest')
        self.ax1.set_title(f'Grid Populasi - Hari {self.model.step_count}')
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')
        
        # Colorbar
        cbar = plt.colorbar(self.mat, ax=self.ax1, shrink=0.8)
        cbar.set_ticks([0, 1, 2, 3])
        cbar.set_ticklabels(['Ignorant', 'Spreader', 'Stifler', 'Resistant'])
        
        # Population plot
        self.ax2.set_title('Dinamika Populasi dari Hari ke-0')
        self.ax2.set_xlabel('Hari')
        self.ax2.set_ylabel('Jumlah Agen')
        
        # Tampilkan statistik awal
        self.display_initial_stats()
        
        plt.tight_layout()
        
    def display_initial_stats(self):
        """Tampilkan statistik awal simulasi"""
        total_agents = len(self.model.schedule.agents)
        resistant_count = sum(1 for a in self.model.schedule.agents 
                            if a.state == GossipState.RESISTANT)
        spreader_count = sum(1 for a in self.model.schedule.agents 
                           if a.state == GossipState.SPREADER)
        
        # Hitung rata-rata koneksi sosial
        avg_connections = np.mean([len(a.social_connections) for a in self.model.schedule.agents 
                                 if a.state != GossipState.RESISTANT])
        
        print(f"Statistik Simulasi:")
        print(f"Total Agen: {total_agents}")
        print(f"Agen Kebal: {resistant_count} ({resistant_count/total_agents*100:.1f}%)")
        print(f"Penyebar Awal: {spreader_count}")
        print(f"Rata-rata Koneksi Sosial: {avg_connections:.1f}")
        print(f"Peluang Penyebaran Lokal: {self.model.spread_probability}")
        print(f"Peluang Penyebaran Global: {self.model.global_spread_probability}")
        print("-" * 50)
        
    def get_grid_state(self):
        """Ambil state grid untuk visualisasi"""
        grid_state = np.zeros((self.model.height, self.model.width))
        
        for agent in self.model.schedule.agents:
            x, y = agent.pos
            grid_state[y, x] = agent.state.value
            
        return grid_state
    
    def update_plots(self):
        """Update plots dengan data terbaru"""
        # Update grid
        self.mat.set_array(self.get_grid_state())
        self.ax1.set_title(f'Grid Populasi - Hari {self.model.step_count}')
        
        # Update population plot
        data = self.model.datacollector.get_model_vars_dataframe()
        
        if len(data) >= 1:  # Tampilkan mulai dari hari ke-0
            days = range(len(data))
            
            self.ax2.clear()
            self.ax2.plot(days, data['Ignorant'], 'o-', color='#4A90E2', 
                         label='Ignorant', linewidth=2, markersize=4)
            self.ax2.plot(days, data['Spreader'], 's-', color='#E24A4A', 
                         label='Spreader', linewidth=2, markersize=4)
            self.ax2.plot(days, data['Stifler'], '^-', color='#4AE24A', 
                         label='Stifler', linewidth=2, markersize=4)
            self.ax2.plot(days, data['Resistant'], 'd-', color='#808080', 
                         label='Resistant', linewidth=2, markersize=4)
            
            self.ax2.set_title(f'Dinamika Populasi - Hari {self.model.step_count}')
            self.ax2.set_xlabel('Hari')
            self.ax2.set_ylabel('Jumlah Agen')
            self.ax2.legend(loc='upper right')
            self.ax2.grid(True, alpha=0.3)
            
            # Set x-axis to show integer days
            self.ax2.set_xticks(range(0, len(data), max(1, len(data)//10)))
    
    def animate(self, frame):
        """Fungsi animasi"""
        # Jangan jalankan step pada frame pertama (frame 0)
        if frame > 0 and self.model.running and self.model.step_count < self.max_steps:
            self.model.step()
            
        self.update_plots()
        return [self.mat]
    
    def run_animation(self):
        """Jalankan animasi"""
        # Update tampilan awal sebelum animasi dimulai
        self.update_plots()
        
        ani = animation.FuncAnimation(self.fig, self.animate, 
                                    frames=self.max_steps + 1,  # +1 untuk frame awal
                                    interval=800, repeat=True, blit=False)
        plt.show()
        return ani

def run_enhanced_gossip_simulation():
    """Jalankan simulasi gosip yang ditingkatkan"""
    
    # Parameter yang dapat disesuaikan
    model = GossipModel(
        width=100,                        # Ukuran grid
        height=100,
        spread_probability=0.3,         # Peluang menyebar gosip ke tetangga fisik
        believe_probability=0.7,         # Peluang percaya dan mulai menyebar
        resistance_rate=0.15,            # Persentase populasi yang kebal
        initial_spreaders=5,             # Jumlah penyebar awal
        global_spread_probability=0.15   # Peluang penyebaran melalui koneksi sosial
    )
    
    # Jalankan visualisasi
    viz = EnhancedGossipVisualization(model, max_steps=30)
    animation_obj = viz.run_animation()
    
    return model, viz, animation_obj

# Jalankan simulasi
if __name__ == "__main__":
    print("Menjalankan Simulasi Penyebaran Gosip yang Ditingkatkan...")
    print("=" * 60)
    print("Fitur Baru:")
    print("• Interaksi global melalui koneksi sosial")
    print("• Setiap agen memiliki 3-15 koneksi sosial")
    print("• Penyebaran melalui telepon/media sosial")
    print("• Menampilkan data mulai dari hari ke-0")
    print("=" * 60)
    print("Keterangan warna:")
    print("🔵 Biru = Ignorant (belum tahu gosip)")
    print("🔴 Merah = Spreader (menyebarkan gosip)")
    print("🟢 Hijau = Stifler (sudah bosan)")
    print("⚪ Abu-abu = Resistant (kebal gosip)")
    print("=" * 60)
    
    model, visualization, animation = run_enhanced_gossip_simulation()
    
    # Simpan animasi jika diperlukan
    animation.save('enhanced_gossip_simulation.mp4', writer='ffmpeg', fps=1, 
                   bitrate=1800, extra_args=['-vcodec', 'libx264'])