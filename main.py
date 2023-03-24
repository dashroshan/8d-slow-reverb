# Utilities
from utils.loadSound import loadSound
from utils.saveSound import saveSound

# Sound effects
from effects.effect8d import effect8d
from effects.slow import effectSlowedDown
from effects.reverb import effectReverb

# Load the sound file
sound = loadSound()

# Add 8d effect
sound8d = effect8d(sound)

# Add slowed down effect
sound8dAndSlowedDown = effectSlowedDown(sound8d)

# Add reverb effect
sound8dSlowedDownReverbed, soundSampleRate = effectReverb(sound8dAndSlowedDown)

# Save the sound file
saveSound(sound8dSlowedDownReverbed, soundSampleRate)

print("8d + slow + reverb effect added successfully!")
