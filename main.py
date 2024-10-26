import requests
import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk

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

def text_to_speech(text: str):
    # Replace with your own subscription key and service region
    speech_key = "YOUR_AZURE_SPEECH_KEY"
    service_region = "YOUR_REGION"

    # Create a speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Create a speech synthesizer with the default speaker output
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Perform the text-to-speech conversion
    print(f"Synthesizing speech for: {text}")
    result = speech_synthesizer.speak_text_async(text).get()

    # Check the result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized successfully.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

if __name__ == "__main__":
    # Example text to synthesize
    text_to_speak = "Hello! This is an example of speech synthesis using Microsoft Azure."
    text_to_speech(text_to_speak)


