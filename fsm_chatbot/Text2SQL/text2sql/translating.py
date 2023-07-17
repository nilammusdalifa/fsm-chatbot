class Translating:
    """
        Kelas ini digunakan untuk memetakan hasil
        parsing menjadi query SQL.
    """
    __where = "WHERE "
    __sql_query = ""
    __select = ""
    __bool_w = False
    __order_condition = ""

    def __init__(self, intent, parsing):
        self.__intent = intent
        self.__parsing = parsing


    def __tanya_stok(self):

        # sql = SELECT stok FROM produk WHERE merk = er['merk'] AND tipe = er['tipe']
        for sql_component in self.__parsing:
            if sql_component[0] == 'SELECT':
                self.__select = str(sql_component[1]).replace('*', 'stok ')
                
            elif sql_component[0] == 'WHERE':
                bool_w = True
                self.__where += sql_component[1] + ''.join(' AND ')

        if self.__select == "":
            return 0

        self.__sql_query = self.__select + 'FROM produk ' + self.__where[:-4]
        return self.__sql_query


    def __tanya_merk(self):

        # apa saja laptop yang tersedia
        # SELECT merk FROM produk
        for sql_component in self.__parsing:
            if sql_component[0] == 'SELECT':
                self.__select = str(sql_component[1]).replace('*', 'DISTINCT merk ')    

        self.__sql_query = self.__select + 'FROM produk '
        return self.__sql_query


    def __tanya_tipe(self):
        
        # apa saja tipe yang tersedia
        # SELECT tipe FROM produk WHERE merk = er['merk'] 
        for sql_component in self.__parsing:

            if sql_component[0] == 'SELECT':
                self.__select = str(sql_component[1]).replace('*', 'tipe ')
                
            elif sql_component[0] == 'WHERE':
                self.__where += sql_component[1] + ''.join(' AND ')

        self.__sql_query = self.__select + 'FROM produk ' + self.__where[:-4]
        return self.__sql_query


    def __tanya_harga(self):
        # berapa harganya
        # SELECT harga FROM produk WHERE merk = er['merk'] AND tipe = er['tipe']
        for sql_component in self.__parsing:

            if sql_component[0] == 'SELECT':
                self.__select = str(sql_component[1]).replace('*', 'harga ')
                
            elif sql_component[0] == 'WHERE':
                self.__where += sql_component[1] + ''.join(' AND ')

        if self.__select == "":
            return 0

        self.__sql_query = self.__select + 'FROM produk ' + self.__where[:-4]
        return self.__sql_query


    def __tanya_spesifikasi(self):
        # spesifikasinya apa
        # spesifikasi laptop er['merk'] er['tipe]
        # sql = SELECT spesifikasi FROM produk WHERE er['merk'] AND er['tipe']
        for sql_component in self.__parsing:
            if sql_component[0] == 'SELECT':
                self.__select = str(sql_component[1]).replace('*', 'prosesor, ram, penyimpanan, layar ')
                
            elif sql_component[0] == 'WHERE':
                self.__where += sql_component[1] + ''.join(' AND ')

        if self.__select == "":
            return 0
        
        self.__sql_query = self.__select + 'FROM produk ' + self.__where[:-4]
        return self.__sql_query


    def __tanya_rekomendasi(self):

        # laptop dengan harga termurah/ termahal
        # sql = SELECT merk, tipe, harga FROM produk 

        # laptop er['merk'] dengan harga termurah/ termahal 
        # sql = SELECT merk, tipe, harga FROM produk WHERE merk = er['merk']

        # a = "SELECT id, merk, tipe, harga FROM produk ORDER BY harga DESC LIMIT 10;"
        for sql_component in self.__parsing:
            for item in sql_component:
                print(self.__parsing)
                if item == 'SELECT':
                    self.__select = str(sql_component[1]).replace('*', 'id, merk, tipe, harga ')

                elif item == 'WHERE':
                    self.__bool_w = True
                    self.__where += sql_component[1] + ''.join(' AND ')

                elif item == 'ORDER_CONDITION':
                    if sql_component[1] == 'termahal':
                        self.__order_condition = 'ORDER BY harga DESC '

                    else:
                        self.__order_condition = 'ORDER BY harga ASC '

        if self.__select == "":
            return 0
        
        # if self.__order_condition == "":
        #     return 1

        if self.__bool_w:
            self.__sql_query = self.__select + 'FROM produk ' + self.__where[:-4] + self.__order_condition + 'LIMIT 5'

        else:
            self.__sql_query = str(self.__select + 'FROM produk ' + self.__order_condition + 'LIMIT 10')

        print(self.__sql_query +"\n")
        return self.__sql_query


    def translate2sql(self):
        if self.__intent == 'tanya_harga': # tanya harga
            self.__sql_query = self.__tanya_harga()
        
        elif self.__intent == 7: # tanya merk
            self.__sql_query = self.__tanya_merk()
        
        elif self.__intent == 'tanya_rekomendasi': # tanya rekomendasi
            self.__sql_query = self.__tanya_rekomendasi()
        
        elif self.__intent == 'tanya_spesifikasi': # tanya spesifikasi
            self.__sql_query = self.__tanya_spesifikasi()
        
        elif self.__intent == 'tanya_stok': # tanya stok
            self.__sql_query = self.__tanya_stok()
        
        elif self.__intent == 12: # tanya tipe
            self.__sql_query = self.__tanya_tipe()


        return self.__sql_query
