# Issue Simulation dengan Mesa

**Issue Simulation** adalah sebuah proyek simulasi penyebaran gosip pada populasi berbasis agen (agent-based modeling) menggunakan framework [Mesa](https://mesa.readthedocs.io/). Proyek ini menggabungkan interaksi lokal (tetangga fisik) dan global (jaringan sosial) untuk memodelkan bagaimana gosip menyebar, berubah menjadi bosan, atau tidak terpengaruh sama sekali. Simulasi dilengkapi dengan antarmuka visual interaktif yang menampilkan grid populasi serta grafik dinamika populasi dari hari ke hari.

---

## Daftar Isi

1. [Deskripsi Proyek](#deskripsi-proyek)
2. [Fitur Utama](#fitur-utama)
3. [Prasyarat](#prasyarat)
4. [Instalasi](#instalasi)
5. [Struktur Proyek](#struktur-proyek)
6. [Deskripsi Modul](#deskripsi-modul)

   * [agent.py](#agentpy)
   * [config.py](#configpy)
   * [model.py](#modelpy)
   * [network.py](#networkpy)
   * [states.py](#statespy)
   * [visualization.py](#visualizationpy)
   * [main.py](#mainpy)
7. [Konfigurasi Simulasi](#konfigurasi-simulasi)

   * [Parameter Umum](#parameter-umum)
   * [Contoh Konfigurasi Kecil / Besar](#contoh-konfigurasi-kecil--besar)
8. [Cara Menjalankan Simulasi](#cara-menjalankan-simulasi)

   * [Mode Interaktif](#mode-interaktif)
   * [Mode Batch](#mode-batch)
   * [Mode Custom](#mode-custom)
   * [Quick Run (Mode Cepat)](#quick-run-mode-cepat)
9. [Opsi dan Argumentasi Pengguna](#opsi-dan-argumentasi-pengguna)
10. [Contoh Penggunaan](#contoh-penggunaan)
11. [Dependensi Eksternal](#dependensi-eksternal)

---

## Deskripsi Proyek

Simulasi ini bermaksud memodelkan dinamika penyebaran gosip di dalam populasi yang tersebar pada grid 2D dengan mekanisme:

* **Interaksi Lokal**: Setiap agen berkomunikasi dengan tetangga fisik dalam radius 1 (Moore neighborhood) dengan probabilitas tertentu.
* **Interaksi Global**: Setiap agen memiliki sejumlah koneksi sosial (3–15 orang) yang membentuk jaringan “small-world” atau “scale-free”. Melalui koneksi ini, gosip dapat menular ke orang yang tidak berada pada grid terdekat.
* **Kepercayaan dan Resistensi**: Agen memiliki probabilitas untuk “percaya” saat pertama kali mendengar gosip, sebelum berubah menjadi “penyebar”. Sebagian kecil agen juga bersifat **resisten**, sehingga tidak akan tertular.
* **Periode Penyebaran & Bosan**: Agen yang telah menjadi penyebar akan menyebarkan gosip selama beberapa hari acak (2–6 hari), kemudian berubah menjadi **dormant** (bosan) dan tidak lagi menyebarkan.
* **Visualisasi**: Simulasi memvisualisasikan kondisi grid setiap langkah (hari) sekaligus grafik jumlah agen dalam tiap status (Uninformed, Spreader, Dormant, Resistant) dari hari ke hari.
* **Opsi Mode**: Terdapat mode interaktif (dengan animasi), mode batch (merekam hasil dalam berbagai format video/GIF), serta mode custom (mengatur parameter kustom), dan quick run (langsung jalan + simpan video).

---

## Fitur Utama

1. **Interaksi Global dan Lokal**

   * Agen dapat menyebarkan gosip ke tetangga fisik (radius 1) dan juga ke koneksi sosial (telepon/media sosial).
   * Jaringan sosial dibangun menggunakan model **Watts-Strogatz (small-world)** atau **Barabási-Albert (scale-free)**.

2. **Status Agen**

   * **UNINFORMED** (biru): Belum tahu gosip.
   * **SPREADER** (merah): Sedang menyebarkan gosip.
   * **DORMANT** (hijau): Pernah menyebar, tapi sudah bosan.
   * **RESISTANT** (abu-abu): Kebal dan tidak akan terpengaruh.

3. **Data Collector**

   * Mengumpulkan statistik jumlah agen per status di setiap langkah (hari).
   * Memudahkan pembuatan grafik dinamika populasi.

4. **Visualisasi Interaktif & Animasi**

   * Menampilkan grid populasi dengan pewarnaan berdasarkan status.
   * Menampilkan grafik populasi per status dari hari ke hari secara real-time.
   * Opsi menyimpan animasi dalam format MP4, AVI, atau GIF.

5. **Konfigurasi Fleksibel**

   * Semua parameter simulasi (ukuran grid, probabilitas, jumlah agen awal, tipe jaringan, dsb) dapat diatur melalui `SimulationConfig` di `config.py`.
   * Tersedia metode pembuatan konfigurasi “kecil” (small test) dan “besar” (large simulation).

6. **Mode Interaktif**

   * Pilih antara “Animasi + save video”, “Save video only”, “Animasi only”, atau “Step-by-step manual”.

7. **Mode Batch & Custom**

   * Mode Batch: generate video dalam berbagai format.
   * Mode Custom: masukkan parameter simulasi secara manual via input console.

---

## Prasyarat

Sebelum menjalankan simulasi, pastikan sistem dan lingkungan Python Anda memenuhi prasyarat berikut:

1. **Python ≥ 3.8**

2. **Pustaka Python (via pip)**:

   * `mesa`
   * `networkx`
   * `numpy`
   * `matplotlib`
   * `dataclasses` (bawaan Python 3.7+; tidak perlu diinstal lagi)

3. **FFmpeg** (opsional)

   * Diperlukan untuk menyimpan animasi dalam format video (`.mp4`, `.avi`, `.mov`).
   * Pastikan `ffmpeg` dapat diakses dari PATH sistem (jika ingin menyimpan video).
   * Untuk menyimpan GIF, cukup instal pustaka `Pillow` (jika belum ada).

---

## Instalasi

1. **Clone repositori ini**

   ```
   git clone https://github.com/fahmiirfanfaiz/modelling-and-simulation-project.git
   cd modelling-and-simulation-project
   ```

2. **Buat lingkungan virtual (opsional, tetapi direkomendasikan)**

   ```
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. **Instal dependensi via pip**

   ```
   pip install mesa networkx numpy matplotlib
   pip install pillow            # Jika ingin menyimpan animasi GIF
   ```

4. **Cek versi**
   Pastikan `matplotlib` dan `mesa` terinstal dengan benar:

   ```bash
   python -c "import mesa; import matplotlib; print(mesa.__version__, matplotlib.__version__)"
   ```

---

## Struktur Proyek

```
modelling-and-simulation-project/
├── gossip_simulation/
│   ├── __init__.py
│   ├── agent.py           # Logika perilaku agen
│   ├── config.py          # Kelas konfigurasi simulasi
│   ├── model.py           # Definisi model utama
│   ├── network.py         # Pembangun & analisis jaringan sosial
│   ├── states.py          # Definisi status dan pemetaan warna
│   ├── visualization.py   # Kelas visualisasi & animasi
│   └── main.py            # Entry point & mode-mode eksekusi
└── README.md              # Dokumentasi (file ini)
```

---

## Deskripsi Modul

### <span id="agentpy"></span>1. `agent.py`

Mengandung definisi kelas `PersonAgent`, yang mengimplementasikan:

* **Atribut**

  * `state`: Status gosip saat ini (`UNINFORMED`, `SPREADER`, `DORMANT`, `RESISTANT`).
  * `days_spreading`: Berapa hari sudah aktif menyebar.
  * `max_spread_days`: Maksimal hari agen akan menyebar sebelum bosan (acak).
  * `social_connections`: Daftar referensi ke agen lain sebagai koneksi sosial.
  * `communication_probability`: Probabilitas agen berkomunikasi lewat koneksi global.

* **Metode Utama**

  * `step()`: Dipanggil setiap iterasi untuk memproses aksi berdasarkan status.
  * `_spread_gossip()`: Menyebarkan gosip ke tetangga fisik (*local*) dan koneksi sosial (*global*).
  * `_listen_for_gossip()`: Mencoba mendengar gosip dari sekitar (tetangga atau koneksi).
  * `hear_gossip()`: Logika agen mendengar gosip—akan berubah jadi `SPREADER` jika `random < believe_probability`.
  * `create_social_connections(connections: List[PersonAgent])`: Menetapkan daftar koneksi sosial dari builder jaringan.

* **Alur**

  1. Jika status `SPREADER`, panggil metode penyebaran lokal dan global, lalu update `days_spreading`.
  2. Jika status `UNINFORMED`, panggil metode untuk mendengar gosip.  

### <span id="configpy"></span>2. `config.py`

Berisi kelas `SimulationConfig` (menggunakan `@dataclass`) yang menyimpan semua parameter simulasi:

```python
@dataclass
class SimulationConfig:
    width: int = 100
    height: int = 100
    spread_probability: float = 0.2
    believe_probability: float = 0.7
    global_spread_probability: float = 0.15
    resistance_rate: float = 0.1
    initial_spreaders: int = 5
    network_type: Literal['small-world', 'scale-free'] = 'scale-free'
    min_social_connections: int = 3
    max_social_connections: int = 15
    min_spread_days: int = 2
    max_spread_days: int = 6
    min_communication_prob: float = 0.1
    max_communication_prob: float = 0.4
    max_steps: int = 30
    animation_interval: int = 800
    save_animation: bool = False
    animation_filename: str = 'enhanced_gossip_simulation.mp4'
    …
```

* **Metode Penting**

  * `validate()`: Memeriksa batas-batas valid (0 ≤ probabilitas ≤ 1, dimensi > 0, dsb).
  * `create_small_test_config()`: Membuat konfigurasi test kecil (20×20 grid, 2 spreaders awal, dsb).
  * `create_large_simulation_config()`: Membuat konfigurasi simulasi skala besar (150×150, 10 spreaders awal).

### <span id="modelpy"></span>3. `model.py`

Mengimplementasi kelas `GossipModel` yang merupakan inti simulasi:

* **Inisialisasi**

  * Validasi konfigurasi, kemudian buat grid 2D (`MultiGrid` dari Mesa) dan scheduler (`RandomActivation`).
  * Panggil `_create_agents()`, `_create_social_network()`, serta `_set_initial_spreaders()`.
  * Setup `DataCollector` untuk mencatat jumlah agen per status di tiap langkah.

* **Metode Utama**

  * `step()`:

    1. Tambah `step_count`.
    2. Panggil `schedule.step()` agar tiap agen menjalankan `step()`.
    3. Kumpulkan data melalui `datacollector.collect(self)`.
    4. Cek apakah simulasi berhenti (jika jumlah penyebar = 0 atau `step_count ≥ max_steps`).

* **Pengambilan Data & Ringkasan**

  * `get_simulation_summary()`: Mengembalikan dictionary berisi jumlah agen per status, persen yang sudah terinformasi, dan apakah simulasi masih berjalan.
  * `get_agents_by_state(state: GossipState)`: Mengembalikan list agen pada status tertentu.

### <span id="networkpy"></span>4. `network.py`

Berisi dua kelas utama:

1. **`SocialNetworkBuilder`**

   * Metode `create_network(agents, config)`:

     * Jika `network_type = 'small-world'` → bangun jaringan Watts-Strogatz.
     * Jika `network_type = 'scale-free'` → bangun jaringan Barabási-Albert.
     * Setelah graf NetworkX dibuat, panggil `_assign_connections_from_graph()` untuk menambahkan koneksi ke tiap agen.

   * Metode `_assign_connections_from_graph(agents, G)`:

     * Untuk setiap agen, ambil daftar neighbor di graf nilai `G`, lalu panggil `agent.create_social_connections()`.

   * Metode `get_network_statistics(agents)`:

     * Hitung statistik jaringan (rata-rata, min, max, std jumlah koneksi selain agen yang `RESISTANT`).

2. **`NetworkAnalyzer`**

   * Metode `analyze_network_structure(agents)`:

     * Konversi koneksi agen menjadi graf NetworkX penuh.
     * Hitung metrik seperti jumlah node, jumlah edge, densitas, apakah terhubung, panjang rata-rata jalur, diameter, clustering coefficient, dsb.
     * Jika graf terputus, analisis komponen terbesar.

### <span id="statespy"></span>5. `states.py`

Mendefinisikan enum `GossipState` untuk status agen:

```python
class GossipState(Enum):
    UNINFORMED = 0    # Belum tahu gosip (biru)
    SPREADER = 1      # Menyebarkan gosip (merah)
    DORMANT = 2       # Sudah bosan gosip (hijau)
    RESISTANT = 3     # Kebal gosip (abu-abu)
```

* **Metode Pendukung**

  * `get_color_mapping()`: Mengembalikan dictionary `{value: hex_color}` untuk pemetaan warna pada visualisasi.
  * `get_state_labels()`: Mengembalikan dictionary `{value: label}` (nama status) untuk legenda.
  * `get_active_states()`, `get_spreading_states()`, `get_receptive_states()`: Mengembalikan daftar status yang aktif, menyebar, atau bisa menerima.

### <span id="visualizationpy"></span>6. `visualization.py`

Kelas `EnhancedGossipVisualization` bertugas menampilkan animasi dan grafik:

* **Inisialisasi**

  * Menerima parameter `model: GossipModel`, `max_steps`, `save_video`, dan `video_filename`.
  * Siapkan palet warna berdasarkan `GossipState.get_color_mapping()`.
  * Buat dua subplot:

    1. `ax1`: Grid populasi (matrix 2D), dengan `imshow`.
    2. `ax2`: Grafik populasi per status dari hari ke-0 (scatter + garis).
  * Tampilkan statistik awal seperti total agen, jumlah agen `RESISTANT`, rata-rata koneksi, probabilitas penyebaran, dsb.

* **Metode Pendukung**

  * `_get_grid_state()`: Menghasilkan array 2D berukuran `height × width` berisi nilai `state.value` tiap agen untuk `imshow`.
  * `_get_population_counts()`: Hitung jumlah agen per status sekarang.
  * `_update_population_display()`: Update teks informasi populasi (total & per status) di atas plot grid, serta teks persentase di grafik.
  * `_update_population_plot()`: Gambar ulang grafik populasi: rumuskan `days = range(len(data))`, plot tiap status dengan marker berbeda.
  * `_update_plots()`: Gabungan meng-update grid (`mat.set_array()`) dan grafik populasi, lalu teks populasi.
  * `animate(frame)`: Fungsi callback untuk `FuncAnimation`; jika i > 0, jalankan satu step simulasi, lalu update plot.
  * `run_animation(show_plot: bool)`: Jalankan animasi selama `max_steps` dengan interval (ms) yang diatur di `config`. Jika `save_video=True`, panggil `save_animation()`.
  * `save_animation(ani, filename)`: Simpan animasi dalam format GIF, MP4, atau AVI sesuai ekstensi.
  * `create_static_plot()`: Buat tampilan statis grid + grafik pada kondisi saat ini.
  * `run_step_by_step()`: Mode manual—pengguna tekan Enter untuk jalankan tiap step, atau 'q' untuk berhenti.
  * `quick_save_video(filename, max_steps)`: Jalankan simulasi tanpa menampilkan plot, langsung menyimpan video.
  * `print_population_summary()`: Cetak ringkasan populasi pada console (total, jumlah tiap status, persentase).

### <span id="mainpy"></span>7. `main.py`

Entry point utama untuk menjalankan simulasi:

* **Fungsi `main()`**

  1. Cetak header informasi (fitur baru, keterangan warna).
  2. Buat objek `SimulationConfig()` (default).
  3. Buat objek `GossipModel(config)`.
  4. Kembalikan `(model, config)`.

* **Mode Eksekusi**

  1. **`run_interactive_simulation()`**

     * Panggil `main()`, lalu tampilkan menu pilihan:

       1. Tampilkan animasi + save video
       2. Hanya save video (tanpa tampilan)
       3. Tampilkan animasi saja
       4. Step-by-step manual
     * Berdasarkan input pilihan, buat `EnhancedGossipVisualization(model, ...)` dan jalankan sesuai mode.
     * Jika input tidak valid, jalankan animasi default.

  2. **`run_batch_simulation()`**

     * Panggil `main()`, buat `EnhancedGossipVisualization`.
     * Jalankan animasi sekali (`show_plot=False`), lalu simpan dalam tiga format:

       * `gossip_hd.mp4` (Video HD)
       * `gossip_quick.gif` (GIF)
       * `gossip_standard.avi` (AVI)

  3. **`run_custom_simulation()`**

     * Panggil `main()`.
     * Minta input: `max_steps` (default `config.max_steps`), apakah `save_video` (y/n), nama file video (jika save).
     * Buat `EnhancedGossipVisualization(model, max_steps, save_video, filename)` sesuai input, lalu `run_animation()`.
     * Jika input tidak valid (ValueError), jalankan animasi default.

  4. **Bagian `if __name__ == "__main__":`**

     * Tampilkan menu awal:

       * A. Interactive Mode
       * B. Batch Mode
       * C. Custom Mode
       * D. Quick Run (langsung jalan + simpan video)
     * Baca input, jalankan fungsi sesuai opsi (default Quick Run jika input tidak terdeteksi).

---

## Konfigurasi Simulasi

Semua parameter utama disimpan di kelas `SimulationConfig` (file `config.py`). Anda dapat menyesuaikan hal-hal berikut:

### <span id="parameter-umum"></span>Parameter Umum

| Parameter                                          | Tipe    | Deskripsi                                                                                   | Default                            |
| -------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------- | ---------------------------------- |
| `width`, `height`                                  | `int`   | Ukuran grid 2D (jumlah sel horizontal dan vertikal).                                        | 100 × 100                          |
| `spread_probability`                               | `float` | Probabilitas agen penyebar menulari tetangga fisik per langkah.                             | 0.2                                |
| `believe_probability`                              | `float` | Probabilitas agen yang mendengar gosip akan “percaya” dan menjadi penyebar.                 | 0.7                                |
| `global_spread_probability`                        | `float` | Probabilitas tambahan penyebaran via koneksi sosial jika agen terpilih berkomunikasi.       | 0.15                               |
| `resistance_rate`                                  | `float` | Persentase awal agen yang bersifat `RESISTANT` (kebal gosip).                               | 0.1                                |
| `initial_spreaders`                                | `int`   | Jumlah agen (non-resistant) yang dijadikan penyebar awal (step 0).                          | 5                                  |
| `network_type`                                     | `str`   | Tipe jaringan sosial: `'small-world'` atau `'scale-free'`.                                  | `'scale-free'`                     |
| `min_social_connections`, `max_social_connections` | `int`   | Jumlah minimum dan maksimum koneksi sosial setiap agen akan dibuat.                         | 3 – 15                             |
| `min_spread_days`, `max_spread_days`               | `int`   | Rentang acak hari maksimum agen akan menyebar sebelum bosan (`DORMANT`).                    | 2 – 6                              |
| `min_communication_prob`, `max_communication_prob` | `float` | Rentang acak probabilitas komunikasi global tiap agen.                                      | 0.1 – 0.4                          |
| `max_steps`                                        | `int`   | Jumlah langkah (hari) maksimal simulasi berjalan (setelah ini, simulasi berhenti otomatis). | 30                                 |
| `animation_interval`                               | `int`   | Interval (ms) antar frame animasi.                                                          | 800                                |
| `save_animation`                                   | `bool`  | Apakah animasi otomatis disimpan saat dijalankan (`True` → simpan, `False` → tidak).        | False                              |
| `animation_filename`                               | `str`   | Nama file animasi video bila opsi `save_animation=True`.                                    | `'enhanced_gossip_simulation.mp4'` |

### <span id="contoh-konfigurasi-kecil--besar"></span>Contoh Konfigurasi

* **Konfigurasi Ukuran Kecil (untuk testing)**

  ```python
  from gossip_simulation.config import SimulationConfig

  config_test = SimulationConfig.create_small_test_config()
  # Menghasilkan: width=20, height=20, max_steps=15, initial_spreaders=2, dsb.
  ```

* **Konfigurasi Skala Besar (untuk simulasi lebih rinci)**

  ```python
  from gossip_simulation.config import SimulationConfig

  config_large = SimulationConfig.create_large_simulation_config()
  # Menghasilkan: width=150, height=150, max_steps=50, initial_spreaders=10, resistance_rate=0.1, dsb.
  ```

* **Menyesuaikan Parameter Secara Manual**

  ```python
  from gossip_simulation.config import SimulationConfig

  config_custom = SimulationConfig(
      width=50,
      height=50,
      spread_probability=0.25,
      believe_probability=0.8,
      global_spread_probability=0.2,
      resistance_rate=0.05,
      initial_spreaders=3,
      network_type='small-world',
      min_social_connections=5,
      max_social_connections=10,
      min_spread_days=3,
      max_spread_days=7,
      min_communication_prob=0.2,
      max_communication_prob=0.5,
      max_steps=40,
      animation_interval=500,
      save_animation=False
  )
  if not config_custom.validate():
      raise ValueError("Parameter konfigurasi tidak valid!")
  ```

---

## Cara Menjalankan Simulasi

### <span id="mode-interaktif"></span>1. Mode Interaktif

Berikut cara menjalankan mode interaktif via `main.py`:

1. **Jalankan Script**

   ```bash
   python main.py
   ```

   Anda akan melihat tampilan:

   ```
   🚀 Gossip Simulation Launcher
   ========================================
   A. Interactive Mode (pilih sendiri)
   B. Batch Mode (semua format)
   C. Custom Mode (atur parameter)
   D. Quick Run (langsung jalan)
   ```

2. **Pilih “A” (Interactive Mode)**
   Setelah menekan `A` + Enter, anda akan melihat:

   ```
   Menjalankan Simulasi Penyebaran Gosip yang Ditingkatkan...
   ==========================================================
   Fitur Baru:
   • Interaksi global melalui koneksi sosial
   • ...
   ==========================================================
   Keterangan warna:
   🔵 Biru = Uninformed (belum tahu gosip)
   🔴 Merah = Spreader (menyebarkan gosip)
   🟢 Hijau = Dormant (sudah bosan)
   ⚪ Abu-abu = Resistant (kebal gosip)
   ==========================================================

   🎮 Pilih mode simulasi:
   1. Tampilkan animasi + save video
   2. Hanya save video (tanpa tampilan)
   3. Tampilkan animasi saja
   4. Step-by-step manual
   Masukkan pilihan (1-4):
   ```

3. **Pilih Opsi**

   * **1**: Menampilkan animasi sekaligus menyimpan video (jika `save_video=True`).

     * Anda dapat memasukkan nama file video (jika kosong, pakai default `gossip_simulation.mp4`).
   * **2**: Hanya menyimpan video tanpa tampilan.

     * Masukkan nama file (default `gossip_quick.mp4`).
   * **3**: Tampilan animasi saja (tanpa save).
   * **4**: Mode step-by-step—Anda tekan Enter setiap kali ingin melanjutkan ke hari berikutnya, ketik `q` untuk keluar.

4. **Simulasi Berjalan**

   * Jendela Matplotlib akan terbuka menampilkan grid dan grafik populasi.
   * Animasi berjalan sesuai `animation_interval` (ms) dan berhenti jika `step_count ≥ max_steps` atau tidak ada lagi penyebar.

### <span id="mode-batch"></span>2. Mode Batch

Mode ini otomatis membuat animasi sekali, lalu menyimpan dalam berbagai format (MP4, GIF, AVI):

1. Jalankan:

   ```bash
   python main.py
   ```
2. Pilih **B** (Batch Mode) + Enter.
3. Konsol akan mencetak:

   ```
   🎯 Mode Batch: Membuat video dalam berbagai format...
   📁 Membuat Video HD: gossip_hd.mp4
   📁 Membuat GIF Animasi: gossip_quick.gif
   📁 Membuat Video AVI: gossip_standard.avi
   ✅ Semua format berhasil dibuat!
   ```

Hasil file tersimpan di direktori kerja saat ini (`gossip_hd.mp4`, `gossip_quick.gif`, `gossip_standard.avi`).

### <span id="mode-custom"></span>3. Mode Custom

Memungkinkan pengguna memasukkan parameter simulasi secara interaktif:

1. Jalankan:

   ```bash
   python main.py
   ```
2. Pilih **C** (Custom Mode) + Enter.
3. Konsol akan meminta input:

   ```
   ⚙️  Mode Custom: Atur parameter simulasi
   Max steps (default 30):
   Save video? (y/n, default n):
   Nama file video:
   ```
4. Masukkan nilai-nilai (jika tekan Enter, akan pakai default).

   * `max_steps`: integer (misal `50`).
   * `save_video`: `y` atau `n`.
   * Jika memilih `y`, masukkan `filename` (misal `custom_simulation.mp4`).
5. Simulasi berjalan sesuai parameter yang baru, kemudian jendela Matplotlib muncul.

Jika input tidak valid (misalnya memasukkan string pada `max_steps`), maka akan muncul pesan error dan dijalankan dengan konfigurasi default.

### <span id="quick-run-mode-cepat"></span>4. Quick Run (Mode Cepat)

Langsung menjalankan simulasi dengan konfigurasi default, menyimpan video, tanpa menampilkan menu:

1. Jalankan:

   ```bash
   python main.py
   ```
2. Ketika menu awal muncul, ketik selain `A`, `B`, atau `C` (misal tekan Enter).

   * Secara otomatis akan masuk ke **Quick Run Mode**.
   * Simulasi berjalan, video disimpan sebagai `gossip_simulation.mp4` di folder kerja.

---

## Opsi dan Argumentasi Pengguna

Sebagai pedoman, berikut opsi-opsi yang dapat dipilih saat menjalankan `main.py`:

| Opsi  | Deskripsi                                                                                     |
| ----- | --------------------------------------------------------------------------------------------- |
| **A** | Interactive Mode: Tampilkan menu simulasi (1–4) sehingga pengguna dapat memilih animasi/step. |
| **B** | Batch Mode: Otomatis membuat video animasi dalam berbagai format (MP4, GIF, AVI).             |
| **C** | Custom Mode: Tanya parameter simulasi (max\_steps, save\_video, dsb) sebelum dijalankan.      |
| **D** | Quick Run: Langsung jalankan animasi + simpan video dengan konfigurasi default.               |

Jika memilih Interactive Mode (A), tersedia sub-opsi:

| Pilihan | Deskripsi                                                    |
| ------- | ------------------------------------------------------------ |
| **1**   | Tampilkan animasi + save video (tanya nama file video).      |
| **2**   | Hanya save video (tanpa tampilkan plot).                     |
| **3**   | Tampilkan animasi saja (tanpa menyimpan video).              |
| **4**   | Mode step-by-step: pengguna tekan Enter tiap langkah (hari). |

---

## Contoh Penggunaan

**Contoh 1:** Menjalankan simulasi default dengan animasi saja

```bash
python main.py   # Pilih A → 3
```

Hasil:

* Jendela Matplotlib muncul, grid + grafik berjalan selama 30 langkah.
* Warna agen berubah sesuai status: biru (UNINFORMED), merah (SPREADER), hijau (DORMANT), abu-abu (RESISTANT).

**Contoh 2:** Menyimpan video simulasi ke `hasil_simulasi.mp4`

```bash
python main.py   # Pilih A → 1, masukkan "hasil_simulasi.mp4"
```

Hasil:

* Simulasi berjalan sambil menampilkan animasi.
* Setelah selesai, file `hasil_simulasi.mp4` tersimpan di direktori kerja.

**Contoh 3:** Mode batch (membuat GIF + MP4 + AVI sekaligus)

```bash
python main.py   # Pilih B
```

Hasil:

* File `gossip_hd.mp4`, `gossip_quick.gif`, dan `gossip_standard.avi` dihasilkan.

**Contoh 4:** Mode custom (ubah `max_steps` menjadi 50, tidak menyimpan video)

```bash
python main.py   # Pilih C
# Input:
# Max steps (default 30): 50
# Save video? (y/n, default n): n
```

Hasil:

* Simulasi berjalan 50 langkah, hanya ditampilkan animasi di jendela Matplotlib, tanpa menyimpan file video.

---

## Dependensi Eksternal

Proyek ini membutuhkan beberapa pustaka eksternal. Berikut daftar lengkap yang direkomendasikan dimasukkan ke dalam `requirements.txt`:

```
mesa>=1.1.1
networkx>=3.0
numpy>=1.20.0
matplotlib>=3.5.0
pillow>=9.0.0        # Jika ingin menyimpan animasi GIF
```

**Catatan:**

* Versi di atas adalah minimal rekomendasi. Versi yang lebih baru biasanya juga kompatibel.
* Untuk opsi menyimpan video, pastikan **FFmpeg** terinstal di sistem dan dapat diakses melalui command line (`ffmpeg` tersedia di PATH).

  * Untuk Windows, unduh dari [ffmpeg.org](https://ffmpeg.org/), lalu tambahkan path `bin/` ke PATH environment.
  * Untuk macOS/Linux, bisa diinstal via package manager (`brew install ffmpeg`, `apt install ffmpeg`, dsb).

---

## Penutup

Dokumentasi terbaru dan segala pembaruan dapat diakses di halaman GitHub:

```
https://github.com/fahmiirfanfaiz/modelling-and-simulation-project
```

Jika ada pertanyaan lebih lanjut, silakan buka issue di repositori atau email ke `developer@example.com`. Selamat menggunakan dan semoga bermanfaat!