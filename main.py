import requests
import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak now...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized speech: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None


def text_to_speech(text, speaker_wav, language):
    url = "http://localhost:8020/tts_to_file/"
    payload = {
        "text": text,
        "speaker_wav": speaker_wav,
        "language": language,
        "file_name_or_path": "output.wav"
    }
    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("TTS API call successful, saving audio...")
            print(response.content)
            return response.content
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None




if __name__ == "__main__":
    text_to_speech("test string", "Ei.wav", "en")