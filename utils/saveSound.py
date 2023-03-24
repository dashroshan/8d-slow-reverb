from settings import *
import soundfile as sf
from os import remove as removeFile
from pydub import AudioSegment


def saveSound(sound, sampleRate):
    """
    Save the sound in MP3 format.
    """

    # Save the sound as WAV
    with sf.SoundFile(
        outputFile + ".wav",
        "w",
        samplerate=sampleRate,
        channels=sound.shape[1],
    ) as f:
        f.write(sound)

    # By default soundfile can only save as WAV, but as WAV files are of large size,
    # we convert it to MP3 format and remove the WAV file.
    AudioSegment.from_wav(outputFile + ".wav").export(outputFile + ".mp3", format="mp3")
    removeFile(outputFile + ".wav")
