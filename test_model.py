from models.buku_model import BukuModel

model = BukuModel()

def tampilkan(judul):
    print(f"\n=== {judul} ===")
    for b in model.get_all_buku():
        print(f"[{b['id_buku']}] {b['judul']} - {b['penulis']} ({b['tahun_terbit']})")

# Siapkan data uji
model.create_buku("Buku Uji Coba", "Penulis Lama", 2000)
id_uji = model.get_all_buku()[-1]['id_buku']

tampilkan("Sebelum Update")

# Test UPDATE
model.update_buku(id_uji, "Buku Uji Coba (Revisi)", "Penulis Baru", 2024)
tampilkan("Setelah Update")

# Test DELETE
model.delete_buku(id_uji)
tampilkan("Setelah Delete")