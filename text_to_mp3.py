import gtts
import sys


def text_to_mp3(text, filename):
    tts = gtts.gTTS(text=text, lang="en")
    tts.save("{}.mp3".format(filename))
    print("Saved as {}.mp3".format(filename))


if __name__ == '__main__':
    text_to_mp3(sys.argv[1], sys.argv[2])
