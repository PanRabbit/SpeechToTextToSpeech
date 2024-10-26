import requests
import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk
from pynput import keyboard

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

def local_text_to_speech(text, speaker_wav, language):
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

def azure_tts(text):
    with open("api.txt") as file:
        key = file.read()
        file.close

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = key
    service_region = "uksouth"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = "en-IE-EmilyNeural"


    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


def main():
    listen_is_on = True
    with keyboard.Events() as events:
        for event in events:
            # Check if the event is a key press and if the key is the backtick
            try:
                if isinstance(event, keyboard.Events.Press) and event.key.char == '`':
                    listen_is_on = not listen_is_on
                    print(listen_is_on)
                elif isinstance(event, keyboard.Events.Press) and event.key.char == 'b' and listen_is_on == True:
                    text = recognize_speech()
                    azure_tts(text)
                else:
                    print('Received event {}'.format(event))
            except:
                print("Womp Womp")


if __name__ == "__main__":
    # text = "Hi, this is Emily"
    # text = recognize_speech()
    # azure_tts(text)
    main()


    #b to start
    #num enter to toggle
