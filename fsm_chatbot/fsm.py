# Flow : loop(input -> detect intent -> change state based on intent -> event handler -> generate response) 
from fsm_chatbot.nlu.intents.intent_detection import IntentDetection
from fsm_chatbot.nlu.entities_recognition.get_entitas import NER
from database.database2 import EcommerceDatabase
from fsm_chatbot.form.login import Login
from fsm_chatbot.form.register import Register
from fsm_chatbot.form.checkout import Checkout
from fsm_chatbot.Text2SQL.text2sql.utility import Text2SQL
from pathlib import Path
from datetime import date
from os.path import dirname, join
import re
import yaml

class FiniteStateMachine:
    def __init__(self):
        self._intent = {
            0: 'login',
            1: 'register',
            2: 'salam_perpisahan',
            3: 'sapa',
            4: 'tambah_barang',
            5: 'tanya_spesifikasi',
            6: 'tanya_harga',
            7: 'tanya_pesan',
            8: 'tanya_rekomendasi',
            9: 'tanya_stok',
            10: 'terima',
            11: 'terimakasih',
            12: 'tolak',
            13: 'unknown'
        }

        # Initialize slot
        self.checkout = Checkout()
        self.login = Login()
        self.regis = Register()

        # Initialize NER
        self.ner = NER()

        self.is_login = False
        self.is_confirm = False
        self.last_msg = []
        
        self.user_request = ''
        self.user_intent = ''
        self._auto_transit = ''
        self.current_state = 'greeting'
        self._valid_states = ['greeting', 'ask', 'ask_stock', 'ask_price', 'ask_specification', 'recommendation', 'auth', 'login', 'register', 'exit', 'order', 'order_detail'] 
        
        # bikin state khusus untuk stok, harga, deskripsi -> klo g tertarik ask state
        # ask state itu untuk response 'apakah ada hal yang bisa saya bantu', klo ga exit
        
        self._transitions = {
            'greeting': {
                'sapa': {
                    'action': self._greeting_state,
                    'next_state': 'greeting'
                }, 
                'tanya_harga': {
                    'action': self.ask_price_state,
                    'next_state': 'ask_price'
                }, 
                'tanya_spesifikasi': {
                    'action': self.ask_specification_state,
                    'next_state': 'ask_specification'
                }, 
                'tanya_stok': {
                    'action': self.ask_stock_state,
                    'next_state': 'ask_stock'
                }, 
                'tanya_rekomendasi': {
                    'action': self._recommendation_state,
                    'next_state': 'recommendation'
                }, 
                'tambah_barang': {
                    'action': self._order_detail_state,
                    'next_state': 'order_detail'
                },
                'tanya_pesan': {
                    'action': self._order_detail_state,
                    'next_state': 'order_detail'
                },
                'salam_perpisahan': {
                    'action': self._exit_state,
                    'next_state': 'exit'
                },
                'unknown': {
                    'action': self._handle_unknown,
                    'next_state': 'greeting' 
                },
                'default': {
                    'action': self._greeting_state,
                    'next_state': 'greeting'
                }
            }, 
            'ask': {
                'tolak': {
                    'action': self._exit_state,
                    'next_state': 'exit'
                }, 
                'tanya_harga': {
                    'action': self.ask_price_state,
                    'next_state': 'ask_price'  
                },
                'tanya_spesifikasi': {
                    'action': self.ask_specification_state,
                    'next_state': 'ask_specification' 
                },
                'tanya_stok': {
                    'action': self.ask_stock_state,
                    'next_state': 'ask_stock'
                },
                'tanya_rekomendasi': {
                    'action': self._recommendation_state,
                    'next_state': 'recommendation', 
                },
                'tambah_barang': {
                    'action': self._order_detail_state,
                    'next_state': 'order_detail' 
                },
                'tanya_pesan': {
                    'action': self._order_detail_state,
                    'next_state': 'order_detail' 
                },
                'salam_perpisahan': {
                    'action': self._exit_state,
                    'next_state': 'exit' 
                },
                'terimakasih': {
                    'action': self._exit_state,
                    'next_state': 'exit' 
                },
                'default': {
                    'action': self._ask_state,
                    'next_state': 'ask'
                }
            },
            'ask_stock':{
                'tolak': {
                    'action': self._ask_state,
                    'next_state': 'ask'
                },
                'terima': {
                    'action': self._order_detail_state,
                    'next_state': 'order_detail'
                },
                'default': {
                    'action': self.ask_stock_state,
                    'next_state': 'ask_stock'
                }
            },
            'ask_price':{
                'tolak': {
                    'action': self._ask_state,
                    'next_state': 'ask'
                },
                'terima': {
                    'action': self._order_detail_state,
                    'next_state': 'order_detail'
                },
                'default': {
                    'action': self.ask_price_state,
                    'next_state': 'ask_price'
                }
            },
            'ask_specification':{
                'tolak': {
                    'action': self._ask_state,
                    'next_state': 'ask'
                },
                'terima': {
                    'action': self._order_detail_state,
                    'next_state': 'order_detail'
                },
                'default': {
                    'action': self.ask_specification_state,
                    'next_state': 'ask_specification'
                }
            },
            'recommendation': {
                'terima': {
                    'action': self._order_detail_state,
                    'next_state': 'order_detail'
                },
                'tolak': {
                    'action': self._ask_state,
                    'next_state': 'ask'
                },
                'salam_perpisahan': {
                    'action': self._exit_state,
                    'next_state': 'exit'
                },
                'terimakasih': {
                    'action': self._exit_state,
                    'next_state': 'exit'
                },
                'default': {
                    'action': self._recommendation_state,
                    'next_state': 'recommendation'
                }
            },
            'auth': {
                'terima': {
                    'action': self._login_state,
                    'next_state': 'login'
                },
                'tolak': {
                    'action': self._register_state,
                    'next_state': 'register'
                },
                'salam_perpisahan': {
                    'action': self._exit_state,
                    'next_state': 'exit'
                },
                'default': {
                    'action': self._auth_state,
                    'next_state': 'auth'
                }
            },
            'login': {
                'default': {
                    'action': self._login_state,
                    'next_state': 'login'
                },
                'tolak': {
                    'action': self._ask_state,
                    'next_state': 'ask'
                },
            },
            'register': {
                'tolak': {
                    'action': self._ask_state,
                    'next_state': 'ask'
                },
                'default': {
                    'action': self._register_state,
                    'next_state': 'register'
                }
            },
            'order_detail':{
                'tolak': {
                    'action': self._ask_state,
                    'next_state': 'ask'
                },
                'default': {
                    'action': self._order_detail_state,
                    'next_state': 'order_detail'
                }
            },
            'order': {
                'terimakasih': {
                    'action': self._exit_state,
                    'next_state': 'exit'
                },
                'salam_perpisahan': {
                    'action': self._exit_state,
                    'next_state': 'exit'
                },
                'tolak': {
                    'action': self._ask_state,
                    'next_state': 'ask'
                },
                'terima': {
                    'action': self._order_state,
                    'next_state': 'order'
                },
                'default': {
                    'action': self._order_state,
                    'next_state': 'order'
                },
            },
            'exit': {
                'default': {
                    'action': self._greeting_state,
                    'next_state': 'greeting'
                }

            }
        }

        # DB Connection
        self._db = EcommerceDatabase('root', 'root', 'localhost', 'db_laptop')

    # STATE HANDLER 
    def _greeting_state(self, user_input, intent):
        return ['Halo, saya focha yang dapat membantu anda dalam pembelian laptop.', 'Anda bisa menanyakan spesifikasi, harga, rekomendasi, stok, dan menambahkan barang ke keranjang anda.', 'Apa yang bisa saya bantu?']

    def _ask_state(self, user_input, intent):
        self.checkout.delete_slot_checkout()
        self.ner.remove_merktipe()
        self.is_confirm = False
        msg = ['Apa yang bisa saya bantu?', 'Anda bisa menanyakan harga, stok, spesifikasi, menambahkan barang, dan meminta rekomendasi laptop']
        
        return msg
            
    def _recommendation_state(self, user_input, intent):
        entity = self._extract_entity(user_input)

        if 'murah' in user_input or 'mahal' in user_input:
            query_result = Text2SQL(entity, 'minta', intent).respond()

            # if query_result == 0:
            #     msg = ['Harap berikan kalimat dengan kata perintah atau kata tanya di dalamnya! Contoh: apa, berikan, minta, tampilkan, dan lain-lain']
            #     return msg
            
            laptop = []
            for item in query_result:
                item_number, brand, model, price = item
                laptop.append(f"{brand} {model}") 
                list_rekom  = self._render_custom_recommendation(laptop)

            msg = ['Berikut rekomendasi laptopnya!', list_rekom, 'Laptop apa yang ingin Anda beli?']
            
            return msg
        
        if entity['merk'] is None:
            all_merk = self._render_all_merk()
            msg = ['Silahkan pilih merk laptop terlebih dahulu!', all_merk, 'Merk laptop apa yang Anda inginkan?']
        else:
            self.checkout.slot['merk'] = entity['merk']
            if entity['tipe'] is None:
                data = self._db.get_recommendation_by_merk((entity['merk'], ))
                tipe = self._render_custom_type(data)
                msg = [f"Berikut 5 rekomendasi tipe laptop terbaik dari {self._get_merk()}", tipe, 'Tipe laptop apa yang ingin Anda beli?']
            else:
                self.checkout.slot['tipe'] = entity['tipe']
        if self.checkout.slot['merk'] and self.checkout.slot['tipe']:
            msg = ['Apakah Anda berminat untuk memesannya sekarang?']

        return msg

    def _order_detail_state(self, user_input, intent):
        entity = self._extract_entity(user_input)
        
        if self.checkout.slot['merk'] is None:
            msg = self._order_merk(entity['merk'])
            if msg:    
                return msg

        if self.checkout.slot['tipe'] is None:
            msg = self._order_tipe(entity['tipe'])
            if msg:
                return msg
        else:
            if len(self.checkout.slot['tipe']) == 1:
                self.checkout.slot['tipe'] = entity['tipe']
                price = self._db.get_price((self._get_merk(), self._get_type()))
                self.checkout.slot['harga'] = price
            else:
                list_tipe = self._render_custom_type(entity['tipe'])
                msg = ['Berikut daftar tipe laptop yang tersedia.', list_tipe, 'Tipe laptop mana yang Anda maksud?']
                self.checkout.slot['tipe'] = None
                self.ner.remove_tipe()

                return msg
     
        if self.checkout.slot['jumlah'] is None:
            msg = self._order_jumlah(user_input)
            if msg:    
                return msg
        
        if self.checkout.slot['merk'] and self.checkout.slot['tipe'] and self.checkout.slot['jumlah']:
            self.ner.remove_merktipe()
            self._auto_transit = 'order'

    def _order_merk(self, merk):
        if merk:
            self.checkout.slot['merk'] = merk
        else:
            all_merk = self._render_all_merk()
            msg = ['Berikut daftar merk laptop yang tersedia di toko kami', all_merk,'Apa merk laptop yang ingin Anda beli?']
            return msg
    
    def _order_tipe(self, tipe):
        if tipe:
            if len(tipe) > 1:
                list_tipe = self._render_custom_type(tipe)
                msg = ['Berikut daftar tipe laptop yang tersedia.', list_tipe, 'Tipe laptop mana yang Anda maksud?']
                self.checkout.slot['tipe'] = None
                self.ner.remove_tipe()

                return msg
            else:
                self.checkout.slot['tipe'] = tipe
        else:
            tipe = self._render_all_type_by_merk(self._get_merk())
            msg = [f"Berikut daftar tipe laptop {self._get_merk()} yang tersedia", tipe, 'Apa tipe laptop yang ingin Anda beli?']

            return msg

    def _order_jumlah(self, jumlah):
        if jumlah.isdigit():
            self.checkout.slot['jumlah'] = int(jumlah)
        else:
            msg = ['Berapa jumlah laptop yang ingin Anda beli?', 'Masukkan format angka. contoh : 1/2/3.']
            return msg

    def _get_order_detail(self):
        merk = self.checkout.slot['merk'].upper()
        tipe = self.checkout.slot['tipe'][0].upper()
        jumlah = self._get_jumlah()
        harga = "Rp. {:,.0f}".format(self._get_price())
        total = "Rp. {:,.0f}".format(self.get_total())

        order_detail = [
            f"<pre>Berikut rincian pesanan Anda \nMerk    : {merk:<10} \nTipe    : {tipe:<10} \nHarga   : {harga:<10} \nJumlah  : {jumlah:<10} \nTotal   : {total:<10} </pre>",
            'Apakah Anda ingin melanjutkan pembelian laptop?'
        ]
        self.is_confirm = True

        return order_detail
    
    def _get_merk(self):
        return self.checkout.slot['merk'].capitalize()
    
    def _get_type(self):
        return self.checkout.slot['tipe'][0].capitalize()
    
    def _get_price(self):
        return self.checkout.slot['harga']
    
    def _get_jumlah(self):
        return self.checkout.slot['jumlah']
    
    def get_total(self):
        return self.checkout.slot['jumlah'] * self.checkout.slot['harga']

    def _generate_nota(self, id_transaksi, tanggal, email, id_laptop, nama_laptop, jumlah, harga, total):
        price = "Rp. {:,.0f}".format(harga)
        total_harga = "Rp. {:,.0f}".format(total)
        msg = f"""
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-7">
                <h1 class="text-lg font-bold text-gray-800">Nota Pembayaran</h1>
                <table class="my-4 text-gray-500 text-xs">
                    <tr>
                        <td>Nomor Pembelian</td>
                        <td> : </td>
                        <td class="font-bold">{id_transaksi}</td>
                    </tr>
                    <tr>
                        <td>Tanggal</td>
                        <td> : </td>
                        <td class="font-bold">{tanggal}</td>
                    </tr>
                    <tr>
                        <td>Status</td>
                        <td> : </td>
                        <td class="font-bold text-red-400">Pending</td>
                    </tr>
                    <tr>
                        <td>Email Pembeli</td>
                        <td> : </td>
                        <td class="font-bold">{email}</td>
                    </tr>
                </table>
                <div class="mb-4">
                    <table class="w-full text-sm">
                        <tr class="border-b border-t">
                            <th class="bg-gray-100 font-bold text-left pl-1 text-gray-600">Id Produk</th>
                            <td class="text-gray-700 pl-2">{id_laptop}</td>
                        </tr>
                        <tr class="border-b">
                            <th class="bg-gray-100 font-bold text-left pl-1 text-gray-600">Produk</th>
                            <td class="text-gray-700 pl-2">{nama_laptop}</td>
                        </tr>
                        <tr class="border-b">
                            <th class="bg-gray-100 font-bold text-left pl-1 text-gray-600">Jumlah</th>
                            <td class="text-gray-700 pl-2">{jumlah}</td>
                        </tr>
                        <tr class="border-b">
                            <th class="bg-gray-100 font-bold text-left pl-1 text-gray-600">Harga</th>
                            <td class="text-gray-700 pl-2">{price}</td>
                        </tr>
                        <tr class="border-b">
                            <th class="font-bold bg-gray-200">Total</th>
                            <td class="font-bold text-gray-800 pl-2">{total_harga}</td>
                        </tr>
                    </table>
                </div>
                <div class="text-gray-500 text-sm mt-2">
                    <p class="mb-2">Terimakasih telah melakukan pemesanan!</p>
                </div>
            </div>
            """

        return msg
    
    def _order_state(self, user_input, intent):
        if intent == 'unknown':
            entity = self.ner.dis
            if len(entity['merk']) == 0 and len(entity['tipe']) == 0 and not user_input.isdigit():
                unknown_msg = self._handle_unknown(user_input, intent)
                try:
                    order_detail_msg = self._get_order_detail()
                except:
                    order_detail_msg = ['Apakah Anda ingin membeli laptop lain?']

                msg = unknown_msg + order_detail_msg
                return msg

        if not self.is_login:
            self._auto_transit = 'auth'
        else:
            if not self.is_confirm:
                msg = self._get_order_detail()
                self.last_msg = msg
                return msg
            else:
                try:
                    res = self.checkout.slot
                    data = (res['merk'], res['tipe'][0])
                    product = self._db.get_product(data)
                    self.checkout.slot['harga'] = product[8]

                    if product:
                        data_transaksi = (self.login.slot['email'], date.today(), product[0], res['jumlah'])
                        new_data_id = self._db.insert_transaction(data_transaksi)
                        
                        if new_data_id['rowcount'] > 0:
                            nota = self._generate_nota(new_data_id['id'][0], date.today(), self.login.slot['email'], product[0], f"{self._get_merk()} {self._get_type()}", self._get_jumlah(), self._get_price(), self.get_total())
                            msg = ['Pemesanan anda berhasil diproses. Berikut nota pembayaran anda', nota, 'Apakah Anda ingin membeli laptop lain?']
                            
                            self.regis.delete_slot_regis()
                            self.checkout.delete_slot_checkout()
                            self.ner.remove_merktipe()
                        else:
                            msg = ['Maaf, pemesanan gagal:(']
                    return msg
                except:
                    self.is_confirm = False
                    self._auto_transit = 'order_detail'
            
    def _auth_state(self, user_input, intent):
        return ['Untuk melanjutkan, silakan login terlebih dahulu. Apakah Anda sudah memiliki akun?']
        
    def _login_state(self, user_input, intent):
        if self.login.slot['email'] is None:
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', user_input):
                self.login.slot['email'] = user_input
            else:
                msg = ['Masukkan informasi berupa alamat email & password untuk melakukan login', 'Pastikan email Anda sesuai dengan format seperti pada contoh yang diberikan! Contoh: nilam@mail.com', 'Masukkan email Anda']
                return msg
            
        if self.login.slot['pass'] is None:
            if re.match(r'^\w+$', user_input):
                self.login.slot['pass'] = user_input
            else:
                msg = ['Masukkan password Anda']
                return msg

        try:
            data = (self.login.slot['email'], self.login.slot['pass'])
            user_is_exist = self._db.user_login(data)

            msg = ['Login berhasil, ' + user_is_exist['name'] + '! Kami senang Anda kembali ke toko online kami.']
            self.is_login = True
            self.ner.dis['merk'] = 'sljdclskc'
            self._auto_transit = 'order' # automatically go to state order
            return msg
        except:
            msg = ['Maaf, email/pass anda salah ☹️', 'Silahkan melakukan login kembali!', 'Masukkan email Anda']
            self.login.delete_slot_login()   
            return msg

    def _register_state(self, user_input, intent):
        if self.regis.slot['nama'] is None:
            if re.match(r'^[A-Z][a-zA-Z\s]+$', user_input):
                self.regis.slot['nama'] = user_input
            else:
                msg = ['Kami akan meminta data seperti nama, email, dan password akun Anda untuk melakukan registrasi akun', 'Masukkan nama Anda sesuai format dari contoh berikut: Nilam Musdalifa']
                return msg
            
        if self.regis.slot['email'] is None:
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', user_input):
                self.regis.slot['email'] = user_input
            else:
                msg = ['Masukkan email Anda', 'Contoh: nilam@mail.com']
                return msg
            
        if self.regis.slot['pass'] is None:
            if re.match(r'^\w+$', user_input):
                self.regis.slot['pass'] = user_input
            else:
                msg = ['Masukkan password']
                return msg
            
        try:
            data = (self.regis.slot['email'], self.regis.slot['pass'], self.regis.slot['nama'])
            rowcount = self._db.add_user(data)
            if rowcount > 0:
                self._auto_transit = 'login'
            else:
                msg = ['Maaf registrasi gagal ☹️', 'Silakan melakukan registrasi ulang dengan memasukkan format berikut: [nama][email][password]', 'Contoh : [Nilam][nilam@mail.com][secret]']
                self.regis.delete_slot_regis()
                return msg
        except:
            msg = ['Email yang Anda masukkan telah terdaftar sebelumnya!', 'Mohon gunakan email yang berbeda']
            self.regis.slot['email'] = None
            self.regis.slot['pass'] = None
            return msg
  
    def _exit_state(self, user_input, intent):
        self.checkout.delete_slot_checkout()
        self.is_confirm = False
        self.ner.remove_merktipe()
        return ['Terima kasih telah menggunakan layanan chatbot ecommerce kami :)', 'Jika Anda memiliki pertanyaan lain di masa depan, jangan ragu untuk kembali lagi. Semoga harimu menyenangkan!']
    
    def _handle_unknown(self, user_input, intent):
        return ['Maaf saya tidak mengerti apa yang kamu maksud...']

    # TRANSITION HANDLER
    def ask_price_state(self, user_input, intent):
        entity = self._extract_entity(user_input)
        if intent == 'tanya_harga':
            self.user_request = user_input
            self.user_intent = intent

        if self.checkout.slot['merk'] and self.checkout.slot['tipe']:
            msg = ['Apakah Anda berminat untuk memesannya sekarang?']

        if entity['merk'] is None:
            all_merk = self._render_all_merk()
            msg = [
                f"Maaf, sepertinya merk tersebut tidak tersedia di toko kami atau merk laptop tidak valid", 
                'Berikut daftar merk laptop yang tersedia di toko kami',
                all_merk,
                'Merk apa yang Anda cari?'
            ]
            return msg
        else:
            self.checkout.slot['merk'] = entity['merk']

        if entity['tipe']:
            if len(entity['tipe']) == 1:
                self.checkout.slot['tipe'] = entity['tipe']

                query_result = Text2SQL(entity, 'berapa', self.user_intent).respond()
                if query_result == 0:
                    msg = ['Harap berikan kalimat dengan kata perintah atau kata tanya di dalamnya! Contoh: apa, berikan, minta, tampilkan, dan lain-lain']
                    return 
                
                for result in query_result:
                    price = result[0]
        
                formatted_price = "Rp. {:,.0f}".format(price)
                msg = [f"Harga laptop {self._get_merk()} {self._get_type()} adalah {formatted_price}.", 'Apakah Anda tertarik?']
            else:
                list_tipe = self._render_custom_type(entity['tipe'])
                msg = ['Berikut daftar tipe laptop yang tersedia.', list_tipe, 'Tipe laptop mana yang Anda maksud?']
                
                self.checkout.slot['tipe'] = None
                self.ner.remove_tipe()

                return msg            
        else:
            list_tipe = self._render_all_type_by_merk(self._get_merk())
            msg = [f"Berikut list laptop {self._get_merk()} dengan tipenya", list_tipe, 'Tipe laptop apa yang ingin Anda beli?']
        
        return msg

    def ask_specification_state(self, user_input, intent):
        entity = self._extract_entity(user_input)

        if intent == 'tanya_spesifikasi':
            self.user_request = user_input
            self.user_intent = intent

        if self.checkout.slot['merk'] and self.checkout.slot['tipe']:
            msg = ['Apakah Anda berminat untuk memesannya sekarang?']

            return msg

        if entity['merk'] is None:
            all_merk = self._render_all_merk()
            msg = [
                f"Maaf, sepertinya merk tersebut tidak tersedia di toko kami atau merk laptop tidak valid", 
                'Berikut daftar merk laptop yang tersedia di toko kami',
                all_merk,
                'Merk apa yang Anda cari?'
            ]

            return msg
        else:
            self.checkout.slot['merk'] = entity['merk']

        if entity['tipe']:
            if len(entity['tipe']) == 1:
                self.checkout.slot['tipe'] = entity['tipe']

                query_result = Text2SQL(entity, 'apa spek', self.user_intent).respond()
                for result in query_result:
                    spec = result
                specification = self._generate_specification_details(self._get_merk(), self._get_type(), spec[0], spec[1], spec[2], spec[3])
                
                msg = [specification, 'Apakah Anda berminat memesannya sekarang?']
                
                return msg
            else:
                list_tipe = self._render_custom_type(entity['tipe'])
                msg = ['Berikut daftar tipe laptop yang tersedia.', list_tipe, 'Tipe laptop mana yang Anda maksud?']
                self.checkout.slot['tipe'] = None
                self.ner.remove_tipe()

                return msg
        else:
            list_tipe = self._render_all_type_by_merk(self._get_merk())
            msg = [f"Silahkan pilih tipe laptop {self._get_merk()} terlebih dahulu", list_tipe, 'Tipe laptop apa yang Anda cari?']

            return msg
    
    def _generate_specification_details(self, merk, tipe, prosesor, ram, penyimpanan, layar):
        msg = f'''
            <div class="flex flex-col gap-2">
                <div class="flex flex-row gap-2">
                    <p>Spesifikasi Laptop</p>
                    <p class="capitalize">{merk} {tipe}</p>
                </div>
                <div class="flex flex-row gap-2">
                    <p class="w-28">Prosesor</p>
                    <p>:</p>
                    <p>{prosesor}</p>
                </div>
                <div class="flex flex-row gap-2">
                    <p class="w-28">RAM</p>
                    <p>:</p>
                    <p>{ram}</p>
                </div>
                <div class="flex flex-row gap-2">
                    <p class="w-28">Penyimpanan</p>
                    <p>:</p>
                    <p>{penyimpanan}</p>
                </div>
                <div class="flex flex-row gap-2">
                    <p class="w-28">Ukuran Layar</p>
                    <p>:</p>
                    <p>{layar}</p>
                </div>
            </div>
        '''

        return msg 
            
    def ask_stock_state(self, user_input, intent):
        entity = self._extract_entity(user_input)

        if intent == 'tanya_stok':
            self.user_request = user_input
            self.user_intent = intent
        
        if entity['merk'] is None:
            all_merk = self._render_all_merk()
            msg = [
                f"Maaf, sepertinya merk tersebut tidak tersedia di toko kami atau merk laptop tidak valid", 
                'Berikut daftar merk laptop yang tersedia di toko kami',
                all_merk,
                'Merk apa yang Anda cari?'  
            ]
            return msg
        else:
            self.checkout.slot['merk'] = entity['merk']

        if entity['tipe']:
            if len(entity['tipe']) == 1:
                self.checkout.slot['tipe'] = entity['tipe']

                query_result = Text2SQL(entity, 'ada', self.user_intent).respond()
                for result in query_result:
                    stok = result[0]
                
                if stok > 0:
                    msg = [f"Stok untuk laptop {self._get_merk()} {self._get_type()} ada {stok} unit", 'Apakah Anda tertarik?']
                else:
                    msg = [f"Mohon maaf, saat ini kami tidak memiliki stok untuk laptop {self._get_merk()} {self._get_type()}."]
                return msg
            else:
                list_tipe = self._render_custom_type(entity['tipe'])
                msg = ['Berikut daftar tipe laptop yang tersedia.', list_tipe, 'Tipe laptop mana yang Anda maksud?']
                self.checkout.slot['tipe'] = None
                self.ner.remove_tipe()

                return msg
                
        else:
            tipe = self._render_all_type_by_merk(self._get_merk())
            msg = [f"Tentu! Ada banyak pilihan untuk laptop {self._get_merk()}", tipe, 'Apa tipe laptop yang Anda cari?']

            return msg
    
    # GET CURRENT STATE
    def get_state(self):
        return self.current_state

    # GET THE NEXT STATE AND EVENT HANDLER
    def respond(self, transition_name, user_input):
        while True:
            if self.current_state in self._valid_states:
                transition = self._transitions[self.current_state]
                next_state = transition.get(transition_name, transition['default'])['next_state']
                event_handler = transition.get(transition_name, transition['default'])['action']
                self.current_state = next_state

                response = event_handler(user_input, transition_name)
            else:
                response = self._handle_unknown(user_input, transition_name)

            if self._auto_transit:
                self.current_state = self._auto_transit
                self._auto_transit = ''
                continue

            break

        return response

    # INTENT DETECTION
    def detect_intent(self, user_input):
        intent_detection = IntentDetection()
        path_model = Path('fsm_chatbot/models/model_v2_SVM.pkl')
        prediction = intent_detection.prediction(path_model, user_input)
        return self._intent[prediction]

    # ENTITIES RECOGNITION
    def _extract_entity(self, user_input):
        entity = self.ner.get_entitas(user_input)

        merk = entity['merk'][0] if len(entity['merk']) == 1 else None

        tipe = []
        if len(entity['tipe']) > 0:
            for item in entity['tipe']:
                for type in item:
                    tipe.append(type)
        else:
            tipe = None

        items = {
            'merk': merk,
            'tipe': tipe
        }

        return items

    def _render_all_merk(self):
        all_merk = self._db.get_all_merk()
        msg = ''
        for merk in all_merk:
            msg += f"""
                <div>
                    <button onclick=handlerButton(this) class="user-input-button rounded-lg min-w-full w-full text-xs border-2 border-sky-500 px-5 py-1 mb-1 font-medium text-sky-500 transition duration-200 hover:bg-sky-600/5 active:bg-sky-700/5">
                        {merk}
                    </button>
                </div>
            """

        return msg
    
    def _render_all_type_by_merk(self, merk):
        all_tipe = self._db.get_type_by_merk((merk, ))
        msg = ''
        for tipe in all_tipe:
            msg += f"""
                <div>
                    <button onclick=handlerButton(this) class="user-input-button rounded-lg min-w-full w-full text-xs border-2 border-sky-500 px-5 py-1 mb-1 font-medium text-sky-500 transition duration-200 hover:bg-sky-600/5 active:bg-sky-500/5">
                        {tipe}
                    </button>
                </div>
            """

        return msg
    
    def _render_custom_type(self, type):
        msg = ''
        for tipe in type:
            msg += f"""
                <div>
                    <button onclick=handlerButton(this) class="user-input-button capitalize rounded-lg min-w-full w-full text-xs border-2 border-sky-500 px-5 py-1 mb-1 font-medium text-sky-500 transition duration-200 hover:bg-sky-600/5 active:bg-sky-700/5">
                        {tipe}
                    </button>
                </div>
            """

        return msg
    
    def _render_custom_recommendation(self, laptop):
        msg = ''
        for item in laptop:
            msg += f"""
                <div>
                    <button onclick=handlerButton(this) class="user-input-button capitalize rounded-lg min-w-full w-full text-xs border-2 border-sky-500 px-5 py-1 mb-1 font-medium text-sky-500 transition duration-200 hover:bg-sky-600/5 active:bg-sky-700/5">
                        {item}
                    </button>
                </div>
            """

        return msg
