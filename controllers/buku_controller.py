import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        self.id_terpilih = None  # id buku yang sedang dipilih di tabel

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol dan tabel
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_logout.configure(command=self.logout)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan tombol aksi
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    # ------------------------------------------------------------------
    # Tabel dan form
    # ------------------------------------------------------------------
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def pilih_baris(self, event=None):
        # Saat baris tabel diklik, isi form dengan data buku tersebut (hanya admin)
        if self.user_role != "admin":
            return
        terpilih = self.view.tabel.selection()
        if not terpilih:
            return
        nilai = self.view.tabel.item(terpilih[0], "values")
        self.id_terpilih = nilai[0]

        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
        self.view.entry_judul.insert(0, str(nilai[1]))
        self.view.entry_penulis.insert(0, str(nilai[2]))
        self.view.entry_tahun.insert(0, str(nilai[3]))

    def kosongkan_form(self):
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
        self.view.tabel.selection_remove(self.view.tabel.selection())
        self.id_terpilih = None

    def ambil_form(self):
        # Mengambil dan memvalidasi isi form. Mengembalikan None jika tidak valid.
        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return None
        if not tahun.isdigit():
            messagebox.showwarning("Peringatan", "Tahun terbit harus berupa angka!")
            return None
        return judul, penulis, tahun

    # ------------------------------------------------------------------
    # Aksi data (khusus admin)
    # ------------------------------------------------------------------
    def simpan_data(self):
        # Proteksi ganda di level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        data = self.ambil_form()
        if data is None:
            return
        judul, penulis, tahun = data

        try:
            if self.model.create_buku(judul, penulis, tahun):
                messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
                self.kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal menyimpan data.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {e}")

    def update_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk mengubah data!")
            return

        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih dulu buku yang akan diperbarui dari tabel!")
            return

        data = self.ambil_form()
        if data is None:
            return
        judul, penulis, tahun = data

        try:
            if self.model.update_buku(self.id_terpilih, judul, penulis, tahun):
                messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
                self.kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal memperbarui data.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih dulu buku yang akan dihapus dari tabel!")
            return

        judul = self.view.entry_judul.get()
        if not messagebox.askyesno("Konfirmasi Hapus", f"Yakin ingin menghapus buku \"{judul}\"?"):
            return

        try:
            if self.model.delete_buku(self.id_terpilih):
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal menghapus data.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    # ------------------------------------------------------------------
    # Navigasi
    # ------------------------------------------------------------------
    def logout(self):
        # Import di dalam method untuk menghindari circular import
        # (auth_controller sudah meng-import buku_controller di bagian atasnya)
        from controllers.auth_controller import AuthController
        self.view.destroy()
        AuthController().run()

    def run(self):
        self.view.mainloop()