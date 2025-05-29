# main.py - Entry point for the gossip simulation
from gossip_simulation.config import SimulationConfig
from gossip_simulation.model import GossipModel
from gossip_simulation.visualization import EnhancedGossipVisualization

def main():
    """Main function to run the gossip simulation"""
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
    
    # Load configuration
    config = SimulationConfig()
    
    # Create model
    model = GossipModel(config)
    
    return model, config


def run_interactive_simulation():
    """Jalankan simulasi dengan pilihan interaktif"""
    model, config = main()
    
    print("\n🎮 Pilih mode simulasi:")
    print("1. Tampilkan animasi + save video")
    print("2. Hanya save video (tanpa tampilan)")
    print("3. Tampilkan animasi saja")
    print("4. Step-by-step manual")
    
    choice = input("Masukkan pilihan (1-4): ").strip()
    
    if choice == "1":
        # Animasi + save video
        print("\n🎬 Mode: Animasi + Save Video")
        filename = input("Nama file video (tekan Enter untuk default): ").strip()
        if not filename:
            filename = "gossip_simulation.mp4"
        
        viz = EnhancedGossipVisualization(
            model, 
            max_steps=config.max_steps,
            save_video=True,
            video_filename=filename
        )
        ani = viz.run_animation()
        
    elif choice == "2":
        # Hanya save video
        print("\n💾 Mode: Save Video Only")
        filename = input("Nama file video (tekan Enter untuk default): ").strip()
        if not filename:
            filename = "gossip_quick.mp4"
        
        viz = EnhancedGossipVisualization(model, max_steps=config.max_steps)
        viz.quick_save_video(filename, max_steps=config.max_steps)
        
    elif choice == "3":
        # Hanya animasi
        print("\n📺 Mode: Animasi Only")
        viz = EnhancedGossipVisualization(model, max_steps=config.max_steps)
        ani = viz.run_animation()
        
    elif choice == "4":
        # Step by step
        print("\n👆 Mode: Step-by-Step")
        viz = EnhancedGossipVisualization(model, max_steps=config.max_steps)
        viz.run_step_by_step()
        
    else:
        print("❌ Pilihan tidak valid, menjalankan mode default...")
        viz = EnhancedGossipVisualization(model, max_steps=config.max_steps)
        ani = viz.run_animation()
    
    print("✅ Simulasi selesai!")


def run_batch_simulation():
    """Jalankan simulasi batch untuk berbagai format"""
    model, config = main()
    
    print("\n🎯 Mode Batch: Membuat video dalam berbagai format...")
    
    viz = EnhancedGossipVisualization(model, max_steps=config.max_steps)
    
    # Buat animasi sekali
    ani = viz.run_animation(show_plot=False)
    
    # Save dalam berbagai format
    formats = [
        ("gossip_hd.mp4", "Video HD"),
        ("gossip_quick.gif", "GIF Animasi"),
        ("gossip_standard.avi", "Video AVI")
    ]
    
    for filename, description in formats:
        print(f"📁 Membuat {description}: {filename}")
        viz.save_animation(ani, filename)
    
    print("✅ Semua format berhasil dibuat!")


def run_custom_simulation():
    """Jalankan simulasi dengan pengaturan kustom"""
    model, config = main()
    
    print("\n⚙️  Mode Custom: Atur parameter simulasi")
    
    # Input parameter kustom
    try:
        max_steps = int(input(f"Max steps (default {config.max_steps}): ") or config.max_steps)
        save_video = input("Save video? (y/n, default n): ").lower().startswith('y')
        
        if save_video:
            filename = input("Nama file video: ").strip() or "custom_gossip.mp4"
            viz = EnhancedGossipVisualization(
                model, 
                max_steps=max_steps,
                save_video=True,
                video_filename=filename
            )
        else:
            viz = EnhancedGossipVisualization(model, max_steps=max_steps)
        
        ani = viz.run_animation()
        
    except ValueError:
        print("❌ Input tidak valid, menggunakan pengaturan default...")
        viz = EnhancedGossipVisualization(model, max_steps=config.max_steps)
        ani = viz.run_animation()


if __name__ == "__main__":
    print("🚀 Gossip Simulation Launcher")
    print("=" * 40)
    print("A. Interactive Mode (pilih sendiri)")
    print("B. Batch Mode (semua format)")
    print("C. Custom Mode (atur parameter)")
    print("D. Quick Run (langsung jalan)")
    
    mode = input("\nPilih mode (A/B/C/D): ").upper().strip()
    
    if mode == "A":
        run_interactive_simulation()
    elif mode == "B":
        run_batch_simulation()
    elif mode == "C":
        run_custom_simulation()
    else:
        # Quick run - mode default
        print("\n⚡ Quick Run Mode")
        model, config = main()
        viz = EnhancedGossipVisualization(
            model, 
            max_steps=config.max_steps,
            save_video=True,
            video_filename="gossip_simulation.mp4"
        )
        ani = viz.run_animation()
        print("✅ Simulasi selesai! Video tersimpan sebagai 'gossip_simulation.mp4'")