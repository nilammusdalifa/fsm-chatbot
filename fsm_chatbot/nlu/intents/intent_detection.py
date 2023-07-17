import math
import os

os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import pickle
from pathlib import Path

class IntentDetection:
    """ Kelas Deteksi Intent """

    ML_NB = 'NAIVE_BAYES'
    ML_SVM = 'SVM'

    __data = None
    __data_test = None
    __data_x = None  # TEXTS
    __data_y = None  # INTENTS

    __train_x = None  # 80%
    __test_x = None  # 20%
    __train_y = None  # 80%
    __test_y = None  # 20%

    __train_y_vect = None  # 80% - label jadi numerik
    __test_y_vect = None  # 20% - label jadi numerik
    __data_y_vect = None  # 100% - label jadi numerik

    __tfidf_vect = None  # data vektor tf-idf
    __train_x_vect = None  # 80% - vektor tf-idf
    __test_x_vect = None  # 20% - vektor tf-idf
    __data_x_vect = None  # 100% - vektor tf-idf

    def __int__(self):
        self.__data = self.__data_test = self.__data_x = self.__data_y = self.__train_x = self.__test_x = self.__train_y = self.__test_y = self.__train_y_vect = self.__test_y_vect = self.__data_y_vect = self.__tfidf_vect = self.__train_x_vect = self.__test_x_vect = self.__data_x_vect = None

    def load_dataset(self, ds_file):
        data = pd.read_csv(ds_file, encoding='latin-1')
        print('\nINFORMASI DATASET')
        print('>>> Lokasi Dataset\t:', os.path.dirname(os.path.abspath(ds_file)))
        print('>>> Nama Dataset\t:', os.path.basename(ds_file))
        print('>>> Jumlah Kolom\t: 2 (KELAS, TEKS)')
        print('>>> Jumlah Baris\t: {} (100%) / {} (80%) / {} (20%)'.format(len(data), math.floor(80 * len(data) / 100),
                                                                           math.ceil(20 * len(
                                                                               data) / 100)))  # lihat floor dan ceil
        self.__data = data

    def __pre_processing(self):
        # print(self.__data_x)
        # print(self.__data_y)
        if (self.__data_x == None) or (self.__data_y == None):
            self.__data['TEKS'] = [t.lower() for t in self.__data['TEKS']]
            self.__data_x = self.__data['TEKS']
            self.__data_y = self.__data['KELAS']
        else:
            print('Fungsi __pre_processing belum dijalankan!')

    def __split_and_encode(self):
        if self.__data_y_vect != []:
            # split dataset
            self.__train_x, self.__test_x, self.__train_y, self.__test_y = model_selection.train_test_split(
                self.__data_x, self.__data_y, test_size=0.2, random_state=25)

            encoder = LabelEncoder()
            self.__train_y_vect = encoder.fit_transform(self.__train_y)
            self.__test_y_vect = encoder.fit_transform(self.__test_y)
            self.__data_y_vect = encoder.fit_transform(self.__data_y)

            # y_asli_encoder = [(self.__data_y[i], self.__data_y_vect[i]) for i in range(0, 50)]
            # sorted(set(y_asli_encoder))
        else:
            print('Fungsi __split_and_selection belum dijalankan!')

    def __vector_space_model(self):
        if self.__data_x_vect != []:
            # buat vektor data untuk train dan test (tf-idf)
            self.__tfidf_vect = TfidfVectorizer(max_features=5000)
            self.__tfidf_vect.fit(self.__data_x)  # vocabulary tf-idf
            self.__train_x_vect = self.__tfidf_vect.transform(self.__train_x)
            self.__test_x_vect = self.__tfidf_vect.transform(self.__test_x)
            self.__data_x_vect = self.__tfidf_vect.transform(self.__data_x)
        else:
            print('Fungsi __vector_space_model belum dijalankan!')

    def __pipeline(self):
        self.__pre_processing()
        self.__split_and_encode()
        self.__vector_space_model()

    def model_training(self):
        model = svm.SVC(kernel='linear', probability=True)
        model_label = self.ML_SVM

        self.__pipeline()

        print('\nPELATIHAN MODEL')
        print('>>> Proses pelatihan model "{}" sedang berjalan, silakan tunggu...'.format(model_label))
        model.fit(self.__train_x_vect, self.__train_y_vect)
        y_pred = model.predict(self.__test_x_vect)
        cm = confusion_matrix(self.__test_y_vect, y_pred)
        print('>>> Proses selesai.')

        path_model = Path('fsm_chatbot/models/model_v2_SVM.pkl')
        file_model = open(path_model, 'wb')
        pickle.dump((model, self.__tfidf_vect), file_model)  # model+vocab (dimensi)

        print('\nINFORMASI PELATIHAN MODEL')
        print('>>> Nama machine learn.\t:', model_label)
        print('>>> Lokasi file model\t:', os.path.abspath(path_model))
        
        # Intent encoder
        y_asli_encoder = [(self.__data_y[i], self.__data_y_vect[i]) for i in range(0, len(self.__data))]
        print('>>> (Kelas, Encoded)\t:', sorted(set(y_asli_encoder)))
        for k, e in sorted(set(y_asli_encoder)):
            print(f'{e}: {k}')

        print('\nINFORMASI HASIL PELATIHAN')
        print(classification_report(self.__test_y_vect, y_pred))

        print('INFORMASI CONFUSION MATRIX')
        print(cm)

        print('Precision: {}'.format(precision_score(self.__test_y_vect, y_pred, average='weighted')))
        print('Recall: {}'.format(recall_score(self.__test_y_vect, y_pred, average='weighted')))
        print('F1-Score: {}'.format(f1_score(self.__test_y_vect, y_pred, average='weighted')))
        print('Accuracy: {}'.format(accuracy_score(self.__test_y_vect, y_pred)))
        
    def prediction(self, path_model, teks):
        # load model
        file = open(path_model, 'rb')
        model, vocab = pickle.load(file)
        d = {'TEKS': [teks]}
        data = pd.DataFrame(data=d)
        data_vek = vocab.transform(data['TEKS'])
        
        # count confidence score
        confidence_scores = model.predict_proba(data_vek)
        predicted_class_index = np.argmax(confidence_scores)
        predicted_class = model.classes_[predicted_class_index]
        predicted_class_score = confidence_scores[0, predicted_class_index]
        print(predicted_class_score)

        if predicted_class_score < 0.6:
            return 13
        else:
            return predicted_class
        
    
    
    
# ds_file = 'H:\\Nilam\\SKRIPSIIIIIIII\\Chatbot\\Project\\chatbot-ecommerce\\flask-fsm-interface\\fsm_chatbot\\data\\dataset_intents_new.csv'
# deteksi_intent = IntentDetection()
# deteksi_intent.load_dataset(ds_file)

# deteksi_intent.model_training()
# deteksi_intent.model_testing()