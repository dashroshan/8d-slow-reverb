from settings import *


def effectSlowedDown(sound):
    """
    Increases sound frame rate to slow it down.
    Returns slowed down version of the sound.
    """

    soundSlowedDown = sound._spawn(
        sound.raw_data,
        overrides={"frame_rate": int(sound.frame_rate * speedMultiplier)},
    )
    soundSlowedDown.set_frame_rate(sound.frame_rate)
    return soundSlowedDown
