# gossip_simulation/visualization.py - Visualization and animation
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from typing import TYPE_CHECKING

from .states import GossipState
from .network import SocialNetworkBuilder

if TYPE_CHECKING:
    from .model import GossipModel

np.random.seed(0)
class EnhancedGossipVisualization:
    """Enhanced visualization for gossip simulation"""
    
    def __init__(self, model: 'GossipModel', max_steps: int = 50, save_video: bool = False, 
                 video_filename: str = "gossip_simulation.mp4"):
        self.model = model
        self.max_steps = max_steps
        self.save_video = save_video
        self.video_filename = video_filename
        
        # Setup colors and visualization
        self._setup_colors()
        self._setup_figure()
        self._display_initial_stats()
        
    def _setup_colors(self) -> None:
        """Setup color mapping for visualization"""
        color_mapping = GossipState.get_color_mapping()
        colors = [color_mapping[i] for i in sorted(color_mapping.keys())]
        self.cmap = ListedColormap(colors)
        
    def _setup_figure(self) -> None:
        """Setup matplotlib figure and axes"""
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(16, 7))
        self.fig.suptitle('Simulasi Penyebaran Gosip dengan Interaksi Global', 
                         fontsize=16, fontweight='bold')
        
        # Grid visualization
        self.mat = self.ax1.imshow(self._get_grid_state(), cmap=self.cmap, 
                                  vmin=0, vmax=3, interpolation='nearest')
        self.ax1.set_title(f'Grid Populasi - Hari {self.model.step_count}')
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')
        
        # Setup colorbar
        self._setup_colorbar()
        
        # Population plot setup
        self.ax2.set_title('Dinamika Populasi dari Hari ke-0')
        self.ax2.set_xlabel('Hari')
        self.ax2.set_ylabel('Jumlah Agen')
        
        # Text objects untuk menampilkan nilai populasi real-time
        self.population_text = self.ax1.text(
            0.02, 0.98, '', transform=self.ax1.transAxes, 
            verticalalignment='top', fontsize=10, 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
            fontweight='bold'
        )
        
        # Text untuk persentase pada plot dinamika
        self.percentage_text = self.ax2.text(
            0.02, 0.98, '', transform=self.ax2.transAxes,
            verticalalignment='top', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7)
        )
        
        plt.tight_layout()
    
    def _setup_colorbar(self) -> None:
        """Setup colorbar for grid visualization"""
        cbar = plt.colorbar(self.mat, ax=self.ax1, shrink=0.8)
        cbar.set_ticks([0, 1, 2, 3])
        
        state_labels = GossipState.get_state_labels()
        labels = [state_labels[i] for i in sorted(state_labels.keys())]
        cbar.set_ticklabels(labels)
        
    def _display_initial_stats(self) -> None:
        """Display initial simulation statistics"""
        total_agents = len(self.model.schedule.agents)
        resistant_count = sum(1 for a in self.model.schedule.agents 
                            if a.state == GossipState.RESISTANT)
        spreader_count = sum(1 for a in self.model.schedule.agents 
                           if a.state == GossipState.SPREADER)
        
        # Calculate network statistics
        network_stats = SocialNetworkBuilder.get_network_statistics(
            list(self.model.schedule.agents)
        )
        
        print(f"Statistik Simulasi:")
        print(f"Total Agen: {total_agents}")
        print(f"Agen Kebal: {resistant_count} ({resistant_count/total_agents*100:.1f}%)")
        print(f"Penyebar Awal: {spreader_count}")
        print(f"Rata-rata Koneksi Sosial: {network_stats['avg_connections']:.1f}")
        print(f"Peluang Penyebaran Lokal: {self.model.config.spread_probability}")
        print(f"Peluang Penyebaran Global: {self.model.config.global_spread_probability}")
        print(f"Tipe Jaringan: {self.model.config.network_type}")
        print("-" * 50)
        
    def _get_grid_state(self) -> np.ndarray:
        """Get current grid state for visualization"""
        grid_state = np.zeros((self.model.config.height, self.model.config.width))
        
        for agent in self.model.schedule.agents:
            x, y = agent.pos
            grid_state[y, x] = agent.state.value
            
        return grid_state
    
    def _get_population_counts(self) -> dict:
        """Get current population counts for each state"""
        counts = {
            'Ignorant': 0,
            'Spreader': 0, 
            'Stifler': 0,
            'Resistant': 0
        }
        
        for agent in self.model.schedule.agents:
            if agent.state == GossipState.IGNORANT:
                counts['Ignorant'] += 1
            elif agent.state == GossipState.SPREADER:
                counts['Spreader'] += 1
            elif agent.state == GossipState.STIFLER:
                counts['Stifler'] += 1
            elif agent.state == GossipState.RESISTANT:
                counts['Resistant'] += 1
                
        return counts
    
    def _update_population_display(self) -> None:
        """Update the real-time population display"""
        counts = self._get_population_counts()
        total = sum(counts.values())
        
        # Text untuk grid (kiri atas)
        population_text = f"POPULASI SAAT INI\n"
        population_text += f"Hari: {self.model.step_count}\n"
        population_text += f"Total: {total}\n\n"
        population_text += f"Ignorant: {counts['Ignorant']}\n"
        population_text += f"Spreader: {counts['Spreader']}\n" 
        population_text += f"Stifler: {counts['Stifler']}\n"
        population_text += f"Resistant: {counts['Resistant']}"
        
        self.population_text.set_text(population_text)
        
        # Text untuk persentase pada plot dinamika
        if total > 0:
            percentage_text = f"PERSENTASE:\n"
            percentage_text += f"Ignorant: {counts['Ignorant']/total*100:.1f}%\n"
            percentage_text += f"Spreader: {counts['Spreader']/total*100:.1f}%\n"
            percentage_text += f"Stifler: {counts['Stifler']/total*100:.1f}%\n"
            percentage_text += f"Resistant: {counts['Resistant']/total*100:.1f}%"
            
            self.percentage_text.set_text(percentage_text)
    
    def _update_plots(self) -> None:
        """Update both grid and population plots"""
        # Update grid visualization
        self.mat.set_array(self._get_grid_state())
        self.ax1.set_title(f'Grid Populasi - Hari {self.model.step_count}')
        
        # Update population plot
        self._update_population_plot()
        
        # Update real-time population display
        self._update_population_display()
    
    def _update_population_plot(self) -> None:
        """Update the population dynamics plot"""
        data = self.model.datacollector.get_model_vars_dataframe()
        
        if len(data) >= 1:
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
            if len(data) > 1:
                self.ax2.set_xticks(range(0, len(data), max(1, len(data)//10)))
            
            # Re-add percentage text setelah clear
            self.percentage_text = self.ax2.text(
                0.02, 0.98, '', transform=self.ax2.transAxes,
                verticalalignment='top', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7)
            )
    
    def animate(self, frame: int) -> list:
        """Animation function called by matplotlib"""
        # Don't run step on first frame (frame 0)
        if frame > 0 and self.model.running and self.model.step_count < self.max_steps:
            self.model.step()
            
        self._update_plots()
        return [self.mat, self.population_text, self.percentage_text]
    
    def run_animation(self, show_plot: bool = True) -> animation.FuncAnimation:
        """Run the animation"""
        # Update initial display
        self._update_plots()
        
        # Create and start animation
        ani = animation.FuncAnimation(
            self.fig, 
            self.animate, 
            frames=self.max_steps + 1,  # +1 for initial frame
            interval=self.model.config.animation_interval, 
            repeat=True, 
            blit=False
        )
        
        # Save animation if requested (prioritas ke parameter konstruktor)
        if self.save_video or getattr(self.model.config, 'save_animation', False):
            self.save_animation(ani, self.video_filename)
        
        # Show the plot
        if show_plot:
            plt.show()
        
        return ani
    
    def save_animation(self, ani: animation.FuncAnimation, filename: str = None) -> None:
        """Save animation to file with multiple format options"""
        if filename is None:
            filename = self.video_filename
            
        # Deteksi format dari ekstensi file
        file_ext = filename.split('.')[-1].lower()
        
        try:
            if file_ext == 'gif':
                print(f"Menyimpan animasi sebagai GIF: {filename}")
                ani.save(filename, writer='pillow', fps=1)
            elif file_ext in ['mp4', 'avi', 'mov']:
                print(f"Menyimpan animasi sebagai video: {filename}")
                ani.save(
                    filename, 
                    writer='ffmpeg', 
                    fps=2, 
                    bitrate=2000, 
                    extra_args=['-vcodec', 'libx264']
                )
            else:
                # Default ke MP4 jika ekstensi tidak dikenali
                filename = filename.rsplit('.', 1)[0] + '.mp4'
                print(f"Format tidak dikenali, menyimpan sebagai MP4: {filename}")
                ani.save(
                    filename, 
                    writer='ffmpeg', 
                    fps=2, 
                    bitrate=2000, 
                    extra_args=['-vcodec', 'libx264']
                )
            
            print(f"✅ Animasi berhasil disimpan: {filename}")
            
        except Exception as e:
            print(f"❌ Error menyimpan animasi: {e}")
            print("💡 Tips:")
            print("   - Pastikan FFmpeg terinstall untuk format video")
            print("   - Gunakan 'pip install pillow' untuk format GIF")
            print("   - Coba format lain jika ada masalah")
    
    def create_static_plot(self) -> None:
        """Create a static plot of current state"""
        self._update_plots()
        plt.show()
    
    def run_step_by_step(self) -> None:
        """Run simulation step by step with user input"""
        print("Press Enter to advance each step, 'q' to quit")
        
        while self.model.running and self.model.step_count < self.max_steps:
            self._update_plots()
            plt.draw()
            plt.pause(0.1)
            
            user_input = input(f"Step {self.model.step_count}: Press Enter to continue (q to quit): ")
            if user_input.lower() == 'q':
                break
                
            self.model.step()
        
        print("Simulation completed!")
        self._update_plots()
        plt.show()
    
    def save_current_animation(self, filename: str = "gossip_animation.mp4") -> None:
        """Save animasi dari state saat ini - fungsi helper"""
        ani = self.run_animation(show_plot=False)
        self.save_animation(ani, filename)
    
    def quick_save_video(self, filename: str = "quick_gossip.mp4", max_steps: int = None) -> None:
        """Jalankan simulasi dan langsung save video tanpa tampilkan plot"""
        if max_steps:
            self.max_steps = max_steps
            
        print(f"🎬 Membuat video simulasi gossip...")
        print(f"📁 File output: {filename}")
        print(f"⏱️  Maksimal steps: {self.max_steps}")
        
        # Set save video dan jalankan tanpa show plot
        self.save_video = True
        self.video_filename = filename
        ani = self.run_animation(show_plot=False)
        
        print("✅ Proses selesai!")
    
    def print_population_summary(self) -> None:
        """Print ringkasan populasi ke console"""
        counts = self._get_population_counts()
        total = sum(counts.values())
        
        print(f"\nRINGKASAN POPULASI - HARI {self.model.step_count}")
        print("=" * 40)
        print(f"Total Agen: {total}")
        print(f"Ignorant:   {counts['Ignorant']:3d} ({counts['Ignorant']/total*100:5.1f}%)")
        print(f"Spreader:   {counts['Spreader']:3d} ({counts['Spreader']/total*100:5.1f}%)")
        print(f"Stifler:    {counts['Stifler']:3d} ({counts['Stifler']/total*100:5.1f}%)")
        print(f"Resistant:  {counts['Resistant']:3d} ({counts['Resistant']/total*100:5.1f}%)")
        print("=" * 40)