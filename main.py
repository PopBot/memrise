import speech_recognition
import speech_recognition as sr
import sys
import pyfiglet
import time
from termcolor import colored
import re
import os
import gtts
from playsound import playsound
from io import BytesIO


def intake(mic, r):
    print(colored("Prepping...", "orange"))
    time.sleep(1)

    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(r, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    print(colored("Listening...", "green"))

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


def analyze_response(text, tokens):
    print(colored("Analyzing response...", "green"))
    print(colored("Response: " + text, "yellow"))
    user_input = text.lower()
    user_input = re.sub(r'[^\w\s]', '', user_input)
    user_input_tokens = user_input.split(" ")
    count_correct = 0
    compare_to = tokens if len(tokens) >= len(user_input_tokens) else user_input_tokens
    compare_of = user_input_tokens if compare_to is tokens else tokens
    tokens_missed = []
    for i in range(len(compare_to)):
        if compare_to[i] == compare_of[i]:
            count_correct += 1
        else:
            tokens_missed.append(compare_to[i])
    print(colored("Correct: " + str(count_correct), "yellow"))
    accuracy = count_correct / len(compare_to)
    print(colored("Accuracy: " + str(accuracy), "yellow"))
    tts = gtts.gTTS(text="You said: " + text, lang="en")
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")

    if accuracy == 1:
        print(colored("You said it correctly!", "green"))
        rtts = gtts.gTTS(text="I'm glad you said that correctly!", lang="en")
        rtts.save("responseAccuracy.mp3")
        playsound("responseAccuracy.mp3")
        os.remove("responseAccuracy.mp3")
        return True
    else:
        print(colored("You said it incorrectly!", "red"))
        base_speech = "Here are the tokens you missed: " + ''.join(tokens_missed)
        rtts = gtts.gTTS(text=base_speech, lang="en")
        rtts.save("responseAccuracy.mp3")
        playsound("responseAccuracy.mp3")
        os.remove("responseAccuracy.mp3")
        time.sleep(2)
        res = "Let's try this again."
        rtts = gtts.gTTS(text=res, lang="en")
        rtts.save("responseAccuracy.mp3")
        playsound("responseAccuracy.mp3")
        os.remove("responseAccuracy.mp3")
        return False


if __name__ == '__main__':
    mp3_fp = BytesIO()
    introduction = pyfiglet.figlet_format("Welcome to MEMRISE!")
    print(colored(introduction, "green"))
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
    print("Number of tokens: " + str(len(tokens)) + "\n\n")
    complete = False
    while not complete:
        response = intake(microphone, recognizer)
        if response["success"]:
            complete = analyze_response(response["transcription"], tokens)
    sys.exit(0)
