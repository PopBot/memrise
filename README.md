# Memrise

Requirements:
- Install PortAudio

> Note: If your PortAudio installation is through Homebrew, you will need to direct pip to the path to install a package requirement (pyaudio), so run
> the following: ```pip install --global-option='build_ext' --global-option="-I$(brew --prefix)/include" --global-option="-L$(brew --prefix)/lib" pyaudio```
> to properly install pyaudio.

To run:
```shell
$ pip install -r requirements.txt
$ python3 memrise.py
```

- [SpeechRecognition library-reference](https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst)