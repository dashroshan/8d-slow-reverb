from pydub import AudioSegment
import soundfile as sf
from pedalboard import (
    Pedalboard,
    Reverb,
)

# Settings
# ----------------------------------------------
inputFile = "music"
outputFile = "music8d"
timeLtoR = 10000
adjust_jump = 5
pan_boundary = 100
volume_multiplier = 6
speed_multiplier = 0.92
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

segment_length = int(timeLtoR / (pan_boundary / adjust_jump * 2))
_8d = sound[0]
pan_limit = []
limit_left = -pan_boundary

for i in range(100):
    if int(limit_left) >= pan_boundary:
        break
    pan_limit.append(limit_left)
    limit_left += adjust_jump

pan_limit.append(pan_boundary)

for i in range(0, len(pan_limit)):
    pan_limit[i] = pan_limit[i] / 100

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


def speed_change(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(
        sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)}
    )
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


_8d = speed_change(_8d, speed_multiplier)
out_f = open(f"{outputFile}.wav", "wb")
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

print("Done!")
