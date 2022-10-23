import numpy as np
import os
import librosa
from IPython.display import Audio
from keras.models import load_model
import warnings
import speech_recognition as sr
warnings.filterwarnings('ignore')

class mic_looping:
    def __init__(self) -> None:
        self.IA_DICT = ['baby', 'ruido']
        self.MODEL_FINAL = load_model('models\model_tratados.h5')
        self.TEST_FILENAME = 'teste.wav'

    #EXTRAI O AUDIO EM MATRIZ
    def extract_mfcc(self, filename):
        y, sr = librosa.load(filename, duration=3, offset=0.5)
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
        return mfcc

    #USA O MODELO DE IA PRA CATEGORIZAR
    def predict(self, filename, emotions):
        audio_extract = [self.extract_mfcc(filename)]
        audio_extract = np.array(audio_extract)
        audio_extract = np.expand_dims(audio_extract, -1)
        result_ia = self.MODEL_FINAL.predict(audio_extract)[0]
        result_dict = {}
        for index, emotion in enumerate(emotions):
            result_dict[emotion] = round(result_ia[index] * 100, 2)
        print(result_dict)
        return result_dict

    #RETORNA A EMOÇÃO COM MAIOR PROBABILIDADE
    def maior_probabilidade(self, predict_dict):
        emocao_final = ''
        probabilidade_final = 0.0
        for emocao, probabilidade in predict_dict.items():
            if (probabilidade > probabilidade_final):
                emocao_final = emocao
                probabilidade_final = probabilidade
        return {emocao_final : round(probabilidade_final * 100, 2)}

    #OUVE O MICROFONE
    def ouvir_microfone(self):
        #Habilita o microfone para ouvir o usuario
        microfone = sr.Recognizer()
        with sr.Microphone() as source:
            microfone.adjust_for_ambient_noise(source)
            audio = microfone.listen(source, phrase_time_limit=3)
            f = open(self.TEST_FILENAME, "wb")
            f.write(audio.get_wav_data())
            f.close()
        return audio
    