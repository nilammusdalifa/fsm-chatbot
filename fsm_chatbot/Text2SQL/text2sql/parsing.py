from fsm_chatbot.Text2SQL.text2sql.kamus import Kamus
from fuzzywuzzy import fuzz

class Parsing:
    """
        Kelas ini digunakan untuk mengidentifikasi
        kata-kata pada teks bahasa alami berdasarkan komponen
        penyususn SQL (Structured Query Language).
    """

    def __identify_word(self, text):
        """
            Fungsi ini digunakan untuk mengidentifikasi
            setiap kata pada teks bahasa alami berdasarkan komponen
            penyusun SQL yang telah didefinisikan pada kamus kata.
        """
        kamus = Kamus().kamus()

        word_list = {}
        for keyword, words in kamus.items():
            for word in words:
                sim_ratio = fuzz.partial_ratio(word, text)

                if sim_ratio >= 80:
                    if keyword not in word_list:
                            word_list[keyword] = []

                    word_list[keyword].append(word)

        return word_list
    

    def __parse2sql_component(self, text, entities):
        """
            Fungsi ini digunakan untuk memparsing entitas 
            dan kata-kata yang telah didentifikasi kedalam
            bentuk penyusun SQL, seperti SELECT, FROM, dan WHERE.
        """

        identified_word = self.__identify_word(text)
        print('word: ', identified_word)

        sql_component = []
        
        # parsing entities
        for entities_name, value in entities.items():
            if value:
                if entities_name == 'tipe':
                    sql_component.append(('WHERE', "{} = '{}'".format(entities_name, value[0])))
                else:
                    sql_component.append(('WHERE', "{} = '{}'".format(entities_name, value)))

        # parsing identified keywoard
        for keywoard, word in identified_word.items():

            if ('tanya' in keywoard) or ('perintah' in keywoard):
                sql_component.append(('SELECT', 'SELECT *'))

            elif 'spesifikasi' in keywoard:
                sql_component.append(('FIELD', 'spesifikasi'))

            elif 'termahal' in keywoard:
                sql_component.append(('ORDER_CONDITION', 'termahal'))  

            elif 'termurah' in keywoard:
                sql_component.append(('ORDER_CONDITION', 'termurah'))

                
        return sql_component
    
    
    def parsing(self, text, entities):
        """
            Melakukan parsing.
        """
        result = self.__parse2sql_component(text, entities)

        return result
    