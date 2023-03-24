from settings import *
import soundfile as sf
from pedalboard import (
    Pedalboard,
    Reverb,
)


def tempAudioFile(sound):
    """
    Pedalboard which is used to add reverb to the sound is incompatible with the in-memory sound object
    used to add the 8d and slowed down effect. Hence, we save it to a temporary WAV file and open it again.
    """

    with open(outputFile + ".wav", "wb") as out_f:
        sound.export(out_f, format="wav")
    audio, sampleRate = sf.read(outputFile + ".wav")
    return audio, sampleRate


def effectReverb(sound):
    """
    Adds reverb effect to the sound.
    """

    # Convert the sound to a format usable by the pedalboard library
    sound, sampleRate = tempAudioFile(sound)

    # Define the reverb settings
    addReverb = Pedalboard(
        [Reverb(room_size=0.8, damping=1, width=0.5, wet_level=0.3, dry_level=0.8)]
    )

    # Add the reverb effect to the sound and return
    reverbedSound = addReverb(sound, sample_rate=sampleRate)
    return reverbedSound, sampleRate
