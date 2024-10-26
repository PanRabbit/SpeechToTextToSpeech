import requests
import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk
from pynput import keyboard

global key
global region
region = "uksouth"

def google_recognize_speech():
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

def azure_speech_recognition():
    # Replace with your Azure Speech service subscription key and region
    subscription_key = key

    # Create a speech configuration object
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    # Create a recognizer with the specified settings
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Say something...")

    # Start recognition
    result = recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech was recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")


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


    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = key
    service_region = region

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
    global key
    with open("api.txt") as file:
        key = file.read()


    listen_is_on = True
    with keyboard.Events() as events:
        for event in events:
            try:
                # Check if the event is a key press and if the key is the backtick
                if isinstance(event, keyboard.Events.Press) and event.key.char == '`':
                    listen_is_on = not listen_is_on
                    print("Listening is now:", listen_is_on)
                elif isinstance(event, keyboard.Events.Press) and event.key.char == 'b' and listen_is_on:
                    text = azure_speech_recognition()
                    azure_tts(text)
                else:
                    print('Received event: {}'.format(event))
            except AttributeError as e:
                print(f"Attribute Womp Womp: {e}. This may occur if a non-character key is pressed.")
            except Exception as e:
                print(f"An unexpected Womp Womp occurred: {e}")


if __name__ == "__main__":
    # text = "Hi, this is Emily"
    # text = recognize_speech()
    # azure_tts(text)
    main()


    #b to start
    # ` to toggle
