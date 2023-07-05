import re
import itertools
import yaml
from pathlib import Path
from fuzzywuzzy import fuzz

class NER():
    
    # dictionary
    dis = {'merk': [],
        'tipe': []
        }

    # dict all merk types
    laptop = {}
    types = []

    file_path = Path('fsm_chatbot/data/produk.yaml')
    with open(file_path, 'r') as file:
        documents = yaml.full_load(file)

    # TIPE digabung dalam satu list
    for item in documents['ENTITAS']:
        list = []
        for i in range(len(item['TIPE'])):
            list.append(item['TIPE'][i])
        laptop[item['MERK']] = list

    # get merk and tipe
    # yaml_to_list()

    # seluruh kombinasi tipe laptop
    type_list = []
    for tipe in laptop:
        list1 = laptop.get(tipe)
        for value in list1:
            list1 = str(value)
            types.append(list1)
            lst = list1.split()
            per = set(itertools.permutations(lst))
            for p in per:
                type_list.append(' '.join(p))

    def __init__(self):
        pass

    def get_entitas(self, words, laptop=laptop, types=types, type_list=type_list):
        txt = words.lower()
        # compiling a pattern for all the combinations of the Models
        regex1one = re.compile(r'\b(?:%s)' % '|'.join(type_list))
        name4 = re.findall(regex1one, txt)
            
        # deteksi merk
        if self.dis['merk'] == []:
            for merk in laptop:
                find_merk = re.search(merk, txt)
                if find_merk:
                    self.dis['merk'].append(merk)
        
        if name4:
            # finding the original model
            type_list1 = []
            for name in name4:
                lst1 = name.split()
                pers = set(itertools.permutations(lst1))
                for per1 in pers:
                    type_list1.append(' '.join(per1))
            self.dis['tipe'].append(list(set(type_list1) & set(types)))

        if self.dis['tipe'] == [] and self.dis['merk']:
            # deteksi entitas tipe
            numerator = 0
            most_similiar_tipe = []
            if self.dis['merk'] == []:
                spesifik_tipe = self.get_all_tipe()
            else:
                spesifik_tipe = self.get_spesifik_tipe()
            for type in spesifik_tipe:
                intersection = list(set(type.split()) & set(words.split()))

                if intersection:
                    if len(intersection) > numerator:
                        numerator = len(intersection)
                        most_similiar_tipe = [type]

                    elif len(intersection) == numerator:
                        most_similiar_tipe.append(type)

                else:
                    sim_ratio = fuzz.WRatio(type, words)

                    if sim_ratio >= 75:
                        most_similiar_tipe.append(type)

            for tipe in most_similiar_tipe:
                self.dis['tipe'].append([tipe])
        
        return self.dis

    def check_match(self):
        match = ''
        # deteksi kecocokan merk & tipe
        for key, value in self.laptop.items():
            for sub_value in value:
                if sub_value == self.dis['tipe'][0][0]:
                    if key == self.dis['merk'][0]:
                        match = 'match'
                    else:
                        match = 'not match'
        return match

    def remove_merktipe(self):
        self.dis['tipe'] = []
        self.dis['merk'] = []

    def remove_tipe(self):
        self.dis['tipe'] = []

    def get_tipe(self, merk):
        return '<ul class="list-disc list-outside ml-5">' + ''.join(['<li>'.rjust(8) + str(name).title() + '</li>' for name in self.laptop[merk]]) + '</ul>'

    # spesifik tipe per merk
    def get_spesifik_tipe(self):
        return self.laptop[self.dis['merk'][0]]

    # get seluruh tipe di db
    def get_all_tipe(self):
        types = []
        for merk in self.laptop:
            for tipe in self.laptop[merk]:
                types.append(tipe)
        
        return types

    # get seluruh merk
    def get_all_merk(self):
        merks = '<ul class="list-disc list-outside ml-5">'
        for merk in self.laptop:
            merks += '<li>' + str(merk).title() + '</li>'
        merks+= '</ul>'
        return merks