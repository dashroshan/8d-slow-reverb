from os import remove as removeFile
from pydub import AudioSegment
import soundfile as sf
from pedalboard import (
    Pedalboard,
    Reverb,
)


# Settings
# ----------------------------------------------
inputFile = "music"  # Name of the file to import
outputFile = "music8d"  # Name of the file to export
timeLtoR = 10000  # Time taken for audio source to move from left to right in ms
jumpPercentage = 5  # Percentage of dist b/w L-R to jump at a time
pan_boundary = 100  # Perctange of dist from center that audio source can go
volume_multiplier = 6  # Max volume DB increase at edges
speed_multiplier = 0.92  # Slowdown audio, 1.0 means original speed, 0.5 half speed etc
# ----------------------------------------------


# Look for and load the input music file
# ----------------------------------------------
try:
    sound = AudioSegment.from_mp3(f"{inputFile}.mp3")
except:
    try:
        sound = AudioSegment.from_wav(f"{inputFile}.wav")
    except:
        print(
            f"File not found!\nRename your music file to '{inputFile}.mp3' or '{inputFile}.wav' and put it in the same folder as this python script."
        )
        exit()
# ----------------------------------------------


# Create a list of values from -1.0 to 1.0
# for panning the audio L to R
# ----------------------------------------------
segment_length = int(timeLtoR / (pan_boundary / jumpPercentage * 2))
_8d = sound[0]
pan_limit = []
limit_left = -pan_boundary

for i in range(100):
    if int(limit_left) >= pan_boundary:
        break
    pan_limit.append(limit_left)
    limit_left += jumpPercentage

pan_limit.append(pan_boundary)

for i in range(0, len(pan_limit)):
    pan_limit[i] = pan_limit[i] / 100
# ----------------------------------------------


# Pan the audio L to R in a loop for 8d effect
# ----------------------------------------------
c = 0
flag = True

for i in range(0, len(sound) - segment_length, segment_length):

    peice = sound[i : i + segment_length]

    if c == 0 and not flag:
        flag = True
        c = c + 2

    if c == len(pan_limit):
        c = c - 2
        flag = False

    volAdjust = volume_multiplier - (
        abs(pan_limit[c]) / (pan_boundary / 100) * volume_multiplier
    )
    peice -= volAdjust

    if flag:
        panned = peice.pan(pan_limit[c])
        c += 1

    else:
        panned = peice.pan(pan_limit[c])
        c -= 1
    _8d = _8d + panned
# ----------------------------------------------


# Slow down the audio
# ----------------------------------------------
def speed_change(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(
        sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)}
    )
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


_8d = speed_change(_8d, speed_multiplier)
# ----------------------------------------------


# Add reverb and save the file as a mp3
# ----------------------------------------------
with open(f"{outputFile}.wav", "wb") as out_f:
    _8d.export(out_f, format="wav")
audio, sample_rate = sf.read(f"{outputFile}.wav")

board = Pedalboard(
    [Reverb(room_size=0.8, damping=1, width=0.5, wet_level=0.3, dry_level=0.8)],
    sample_rate=sample_rate,
)
effected = board(audio)

with sf.SoundFile(
    f"./{outputFile}.wav",
    "w",
    samplerate=sample_rate,
    channels=effected.shape[1],
) as f:
    f.write(effected)

AudioSegment.from_wav(f"{outputFile}.wav").export(f"{outputFile}.mp3", format="mp3")
removeFile(f"{outputFile}.wav")
# ----------------------------------------------

print("Done!")
