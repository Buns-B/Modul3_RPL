#from controllers.anggota_controller import AnggotaController
from controllers.buku_controller import BukuController

if __name__ == "__main__":
    #app = AnggotaController()
    app = BukuController()
    app.run()