<!-- SKENARIO -->
USER: Apa leptop lenovo masih ada?
BOT: 
    intent  : tanya_stok
    entitas : lenovo
    proses  : SELECT tipe FROM produk WHERE merk = lenovo AND stok > 0
    respon  :
        - apa tipe laptop {entitas.merk}-nya? //  entitas.merk = lenovo
        - tampilkan tipe-tipe laptop {entitas.merk}
USER: Thinkpad
BOT:
    entitas : Thinkpad
    proses  : SELECT stok FROM produk WHERE merk = lenovo AND stok > 0
    respon  :
        - Laptop {entitas.merk} tipe {entitas.tipe} masih ada, stoknya masih {stok}


KEMUNGKINAN SKENARIO
1. USER MENGISI SEMUA SLOT
2. USER MENGISI SATU PER SATU