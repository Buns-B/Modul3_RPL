import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()
        self.id_terpilih = None

        # Binding (mengikat) tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan tabel di View terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Mengambil data dari Model (database)
        data_buku = self.model.get_all_buku()

        # Memasukkan data ke tabel di View
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def simpan_data(self):
        # Mengambil teks dari input di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        # Validasi Form Kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        # Mengirim data ke Model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            # Bersihkan form input
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            # Muat ulang tabel agar data baru muncul
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def pilih_baris(self, event):
        # Ambil baris yang sedang diklik di tabel
        terpilih = self.view.tabel.selection()
        if not terpilih:
            return

        # Ambil isi baris tersebut: urutannya (id, judul, penulis, tahun)
        data = self.view.tabel.item(terpilih[0])['values']

        # Simpan id_buku ke "kotak" tadi
        self.id_terpilih = data[0]

        # Tampilkan isi baris ke form supaya bisa diedit
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_judul.insert(0, data[1])
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_penulis.insert(0, data[2])
        self.view.entry_tahun.delete(0, 'end')
        self.view.entry_tahun.insert(0, data[3])

    def update_data(self):
        # Cek dulu: sudah ada baris yang dipilih atau belum
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih dulu buku di tabel yang mau diperbarui!")
            return

        # Ambil teks terbaru dari form
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        # Validasi form kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        # Kirim ke Model: id_buku dulu, lalu data barunya
        berhasil = self.model.update_buku(self.id_terpilih, judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            # Bersihkan form dan lupakan baris yang dipilih
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.id_terpilih = None
            # Muat ulang tabel agar perubahan muncul
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self):
        # Cek dulu: sudah ada baris yang dipilih atau belum
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih dulu buku di tabel yang mau dihapus!")
            return

        # Tanya konfirmasi supaya tidak terhapus karena salah klik
        yakin = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus buku ini?")
        if not yakin:
            return

        # Kirim id_buku ke Model untuk dihapus
        berhasil = self.model.delete_buku(self.id_terpilih)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            # Bersihkan form dan lupakan baris yang dipilih
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.id_terpilih = None
            # Muat ulang tabel agar data yang dihapus hilang
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")
            
    def run(self):
        self.view.mainloop()