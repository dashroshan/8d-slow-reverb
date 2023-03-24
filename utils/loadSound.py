from settings import *
from os.path import isfile
from pydub import AudioSegment


def loadSound():
    """
    Loads and returns the MP3 or WAV (whichever is found) source sound file.
    Stops program execution if file not found.
    """

    if isfile(inputFile + ".mp3"):
        return AudioSegment.from_mp3(inputFile + ".mp3")
    elif isfile(inputFile + ".wav"):
        return AudioSegment.from_wav(inputFile + ".wav")
    else:
        print("Source music file not found!")
        exit()
