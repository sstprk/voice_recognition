import speech_recognition as sr
from pydub import AudioSegment


class asd():
    def SestenMetinYapma(self, file_path):
        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(file_path) as source:
                audio = recognizer.record(source)

            metin = recognizer.recognize_google(audio, language='tr-TR')  # Türkçe için 'tr-TR' kullanılıyor

            with open("output.txt", "w", encoding="utf-8") as dosya: dosya.write(metin)

            self.BilgilendirmeKutusu.setText("Metin başarıyla kaydedildi.")
        except sr.UnknownValueError:
            self.BilgilendirmeKutusu.setText("Ses tanınamadı.")
        except sr.RequestError as e:
            self.BilgilendirmeKutusu.setText(f"Google API'den yanıt alınamadı; {e}")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(f"Bir hata oluştu: {e}")