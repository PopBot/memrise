import speech_recognition
import speech_recognition as sr
import sys
from pydub import AudioSegment
from termcolor import colored
from pydub.playback import play
import re
import os
import gtts
from playsound import playsound
from io import BytesIO


def intake(mic, r, memorize_phrase):

    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(r, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=3)
        audio = r.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = r.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    print(response)
    return response


if __name__ == '__main__':
    mp3_fp = BytesIO()
    intro = colored("Welcome to MEMRISE", "green", attrs=["bold"])
    print("Welcome to MEMRISE.")
    mics = speech_recognition.Microphone().list_microphone_names()
    print("Available microphones:")
    for i, mic in enumerate(mics):
        print(f"{i}: {mic}")
    mic_index = 0
    try:
        mic_index = int(input("Enter the index of the microphone: "))
    except ValueError:
        mic_index = 0
        print("Using default microphone at index 0.")

    microphone = sr.Microphone(device_index=mic_index)
    recognizer = sr.Recognizer()
    phrase = input("Enter the phrase you want to memorize: ")
    print("You entered: \n" + phrase)
    tts = gtts.gTTS(text=phrase, lang="en")
    filename = "input.mp3"
    tts.write_to_fp(mp3_fp)
    tts.save(filename)
    playsound(filename)
    os.remove(filename)
    # song = AudioSegment.from_file(mp3_fp)
    # play(song)
    phrase = phrase.lower()
    phrase = re.sub(r'[^\w\s]', '', phrase)
    phrase_length = len(phrase)
    tokens = phrase.split(" ")
    print("Tokens: " + str(tokens))

    # intake(microphone, recognizer)
