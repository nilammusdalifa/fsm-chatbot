from fsm_chatbot.Text2SQL.text2sql.parsing import Parsing
from fsm_chatbot.Text2SQL.text2sql.translating import Translating
from database.database2 import EcommerceDatabase

class Text2SQL:
    """
        Ini adalah kelas chat.
        Kelas ini digunakan untuk menampung dan 
        memproses teks bahasa alami kedalam fungsi-fungsi
        yang telah dideklarasikan.
    """

    def __init__(self, entities, text, intent):

        self.__entities = entities
        self.__text = text
        self.__intent = intent
        self.__parsing = Parsing()
        self.__db = EcommerceDatabase('root', 'root', 'localhost', 'db_laptop')

    def __get_parsing(self):

        parsing = self.__parsing.parsing(self.__text, self.__entities)
        return parsing

    def __get_query(self):
        parsing = self.__get_parsing()
        translating = Translating(self.__intent, parsing)

        return translating.translate2sql()
    
    def respond(self):
        query = self.__get_query()
        print(query)
        if isinstance(query, int):
            result = query
        else:
            result = self.__db.query(query)

        return result