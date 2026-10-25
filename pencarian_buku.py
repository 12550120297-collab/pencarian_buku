import csv
import time

# ====== PENGATURAN (sesuaikan dengan nama kolom di books.csv) ======
FILE_CSV = "books.csv"
KOLOM_JUDUL = "Title"
KOLOM_PENULIS = "Author"
KOLOM_KATEGORI = "Category"


# ====== KELAS INPUT: 1 data buku ======
class Buku:
    def __init__(self, no, judul, penulis, kategori):
        self.no = no
        self.judul = judul
        self.penulis = penulis
        self.kategori = kategori
        self.kunci = judul.lower().strip()   # dipakai untuk membandingkan


# ====== KELAS OUTPUT: hasil 1 kali pencarian ======
class Hasil:
    def __init__(self, ditemukan, buku, perbandingan):
        self.ditemukan = ditemukan           # True / False
        self.buku = buku                     # objek Buku atau None
        self.perbandingan = perbandingan     # jumlah perbandingan
        self.waktu = 0.0                     # detik


# ====== 1. BACA DATASET -> disimpan di list ======
def baca_dataset(nama_file):
    data = []
    with open(nama_file, encoding="utf-8", newline="") as f:
        pembaca = csv.DictReader(f)
        for i, baris in enumerate(pembaca):
            data.append(Buku(i + 1, baris[KOLOM_JUDUL],
                             baris[KOLOM_PENULIS], baris[KOLOM_KATEGORI]))
    return data


# ====== 2. LINEAR SEARCH ======
def linear_search(data, judul):
    target = judul.lower().strip()
    hitung = 0
    for buku in data:
        hitung += 1                          # 1 perbandingan tiap elemen
        if buku.kunci == target:
            return Hasil(True, buku, hitung)
    return Hasil(False, None, hitung)


# ====== 3. BINARY SEARCH (data HARUS sudah terurut) ======
def binary_search(data, judul):
    target = judul.lower().strip()
    kiri, kanan = 0, len(data) - 1
    hitung = 0
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        hitung += 1                          # 1 perbandingan tiap putaran
        if data[tengah].kunci == target:
            return Hasil(True, data[tengah], hitung)
        elif data[tengah].kunci < target:
            kiri = tengah + 1                # buang separuh kiri
        else:
            kanan = tengah - 1               # buang separuh kanan
    return Hasil(False, None, hitung)


# ====== 4. UKUR WAKTU (diulang 20x lalu dirata-rata) ======
def jalankan(fungsi, data, judul):
    hasil = fungsi(data, judul)
    mulai = time.perf_counter()
    for _ in range(20):
        fungsi(data, judul)
    hasil.waktu = (time.perf_counter() - mulai) / 20
    return hasil


# ====== 5. TAMPILKAN HASIL ======
def tampilkan(nama, judul, hasil):
    print(f"[{nama}] mencari: {judul}")
    if hasil.ditemukan:
        b = hasil.buku
        print("  DITEMUKAN")
        print("  No       :", b.no)
        print("  Judul    :", b.judul)
        print("  Penulis  :", b.penulis)
        print("  Kategori :", b.kategori)
    else:
        print("  TIDAK DITEMUKAN")
    print("  Perbandingan:", hasil.perbandingan)
    print(f"  Waktu       : {hasil.waktu * 1000:.6f} ms\n")


# ====== PROGRAM UTAMA ======
semua = baca_dataset(FILE_CSV)
print("Jumlah buku:", len(semua), "\n")

# --- contoh pencarian ---
terurut = sorted(semua, key=lambda b: b.kunci)   # urutkan dulu untuk Binary Search
contoh = semua[len(semua) // 3].judul
tampilkan("Linear Search", contoh, jalankan(linear_search, semua, contoh))
tampilkan("Binary Search", contoh, jalankan(binary_search, terurut, contoh))
tidak_ada = "### judul tidak ada ###"
tampilkan("Linear Search", tidak_ada, jalankan(linear_search, semua, tidak_ada))
tampilkan("Binary Search", tidak_ada, jalankan(binary_search, terurut, tidak_ada))

# --- pengujian n = 100, 1000, 10000 ---
print(f"{'n':>6} {'Algoritma':<14} {'Skenario':<16} {'Perbandingan':>12} {'Waktu (ms)':>12}")
print("-" * 66)
for n in [100, 1000, 10000]:
    sub = semua[:n]
    sub_urut = sorted(sub, key=lambda b: b.kunci)
    uji = [
        ("Linear Search", linear_search, sub, sub[0].judul, sub[n // 2].judul, sub[-1].judul),
        ("Binary Search", binary_search, sub_urut, sub_urut[0].judul,
         sub_urut[(n - 1) // 2].judul, sub_urut[-1].judul),
    ]
    for nama, fungsi, data, awal, tengah, akhir in uji:
        for skenario, judul in [("Awal", awal), ("Tengah", tengah),
                                ("Akhir", akhir), ("Tidak ditemukan", tidak_ada)]:
            h = jalankan(fungsi, data, judul)
            print(f"{n:>6} {nama:<14} {skenario:<16} {h.perbandingan:>12} {h.waktu * 1000:>12.6f}")
    print("-" * 66)
