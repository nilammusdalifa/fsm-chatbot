import yaml
from os.path import dirname, join

class Kamus:

    def __kamus_data(self):
        current_dir = dirname(__file__)
        file_path = join(current_dir,"../../data/kamus_kata.yaml")
        with open(file_path, 'r') as f:
            kamus_kata = yaml.full_load(f)

        return kamus_kata
    

    def kamus(self):
        kamus_kata = self.__kamus_data()
        list_kamus = {}

        for keyword in kamus_kata['KAMUS']:
            word_list = []
            for word in keyword['WORD']:
                word_list.append(word.lower())
            list_kamus[keyword['KEYWORD']] = word_list

        return list_kamus