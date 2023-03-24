# Utilities
from utils.loadSound import loadSound
from utils.saveSound import saveSound

# Sound effects
from effects.effect8d import effect8d
from effects.slow import effectSlowedDown
from effects.reverb import effectReverb

sound = loadSound()
sound8d = effect8d(sound)
sound8dAndSlowedDown = effectSlowedDown(sound8d)
sound8dSlowedDownReverbed, soundSampleRate = effectReverb(sound8dAndSlowedDown)
saveSound(sound8dSlowedDownReverbed, soundSampleRate)

print("8d + slow + reverb effect added successfully!")
