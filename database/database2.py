import mysql.connector

class EcommerceDatabase:
    def __init__(self, user, password, host, database):
        self._user = user
        self._password = password
        self._host = host
        self._database = database

    def connect(self):
        self.connection = mysql.connector.connect(user=self._user, password=self._password,
                              host=self._host,
                              database=self._database)
        
    def disconnect(self):
        self.connection.close()

    def query(self, sql_query):
        output = []
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            print(result)

            if cursor.rowcount > 0:
                # output.extend(result)
                for item in result:
                    print(item)
                    output.append(item)
            else:
                output.append('Maaf poduk yang Anda cari tidak tersedia')
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()

                
        return output

    def get_recommendation_by_merk(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT tipe FROM produk WHERE merk LIKE %s ORDER BY harga DESC LIMIT 5", data)
            results = cursor.fetchall()
            product_recommendation = []

            for result in results:
                product_recommendation.append(result[0]) 

            print(product_recommendation)

            return product_recommendation   
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()

    def get_price(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT harga FROM produk WHERE merk LIKE %s AND tipe LIKE %s", data)
            result = cursor.fetchone()
            price = {
                'price': result[0]
            }

            return price
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()
    
    def get_stock(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT tipe, stok FROM produk WHERE merk LIKE %s AND tipe LIKE %s", data)
            result = cursor.fetchall()

            for stock in result:
                stok = stock[1] 
            
            if len(result) < 1:
                stok = None
        
            return stok
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()
    
    def get_type_by_merk(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT tipe FROM produk WHERE merk LIKE %s AND stok > 0", data)
            results = cursor.fetchall()
            tipe = []

            for type in results:
                tipe.append(type[0])  
            
            if len(results) < 1:
                tipe = None

            return tipe
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()

    def get_price_type_by_merk(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT tipe, harga FROM produk WHERE merk LIKE %s AND stok > 0", data)
            results = cursor.fetchall()
            price = []

            for type in results:
                price.append(f"{type[0]}" + " : " + "Rp. {:,.0f}".format(type[1]))  
            
            if len(results) < 1:
                price = None

            return price
        
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()
    
    def get_description(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT prosesor, ram, penyimpanan, layar FROM produk WHERE merk LIKE %s AND tipe LIKE %s", data)
            description = cursor.fetchone()
            result = {
                'prosesor': description[0],
                'ram': description[1],
                'penyimpanan': description[2],
                'layar': description[3],
            }

            return result
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()
    
    def find_email(self, email):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT email FROM pengguna WHERE email = '{email}'")
            results = cursor.fetchall()
            email = []

            for result in results:
                email.append(result[0])

            return len(email) > 0
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()

    def user_login(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM pengguna WHERE email = %s AND pass = %s", data)
            user = cursor.fetchone()
            
            if user:
                result = {
                    'email': user[0],
                    'pass': user[1],
                    'name': user[2],
                }
            else:
                result = None

            return result
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()

    def add_user(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO pengguna (email, pass, nama) VALUES (%s, %s, %s)", data)
            self.connection.commit()

            return cursor.rowcount
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()

    def get_all_merk(self):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT distinct(merk) FROM produk")
            results = cursor.fetchall()
            merk = []

            for item in results:
                merk.append(item[0])

            return merk
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()

    def get_product(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM produk WHERE merk = %s AND tipe = %s", data)

            product = cursor.fetchone()

            return product
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()
    
    def insert_transaction(self, data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO transaksi (email, tanggal, id_produk, jumlah) VALUES (%s, %s, %s, %s)", data)
            self.connection.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            id = cursor.fetchone()
            rowcount = cursor.rowcount

            return {
                'id': id,
                'rowcount': rowcount
            }
        except mysql.connector.Error as error:
            print(f"Error retrieving data from the database: {error}")
        finally:
            self.disconnect()
    