import speech_recognition as sr
import requests
import base64

class MicRecord:
    def __init__(self) -> None:
        pass
    
    #OUVE O MICROFONE
    def ouvir_microfone(self):
        #Habilita o microfone para ouvir o usuario
        microfone = sr.Recognizer()
        with sr.Microphone() as source:
            microfone.adjust_for_ambient_noise(source)
            audio = microfone.listen(source, phrase_time_limit=3)
            return base64.b64encode(audio.get_wav_data())

    def chamar_api(self):
        audio_b64 = self.ouvir_microfone()
        payload = {
            "audio_b64" : audio_b64
        }
        api = requests.post(url='https://tcc-babysitter.herokuapp.com/classificar', data=payload)