from settings import *


def panArray():
    """
    Generates an array of range -1.0 to 1.0 which control the position of audio source (pan effect).
    -1.0 places the audio source on extreme left, 0.0 on center, and 1.0 on extreme right.
    The audio is splitted into multiple pieces and each piece is played from an position decided by this array.

    Returns pan position array along with the time length of each piece to play at one position.
    """

    # Total pieces when audio source moves from center to extreme right
    piecesCtoR = panBoundary / jumpPercentage

    # Total pieces when audio source moves from extreme left to extreme right
    piecesLtoR = piecesCtoR * 2

    # Time length of each piece
    pieceTime = int(timeLtoR / piecesLtoR)

    pan = []
    left = -panBoundary  # Audio source to start from extreme left

    while left <= panBoundary:  # Until audio source position reaches extreme right
        pan.append(left)  # Append the position to pan array
        left += jumpPercentage  # Increment to next position

    # Above loop generates number in range -100 to 100, this converts it to -1.0 to 1.0 scale
    pan = [x / 100 for x in pan]
    return pan, pieceTime


def effect8d(sound):
    """
    Generates the 8d sound effect by splitting the audio into multiple smaller pieces,
    pans each piece to make the sound source seem like it is moving from L to R and R to L in loop,
    decreases volume towards center position to make the movement sound like it is a circle
    instead of straight line.
    """

    # Get the pan position array and time length of each piece to play at one position
    pan, pieceTime = panArray()

    sound8d = sound[0]  # Stores the 8d sound
    panIndex = 0  # Index of current pan position of pan array

    # We loop through the pan array forward once, and then in reverse (L to R, then R to L)
    iteratePanArrayForward = True

    # Loop through starting time of each piece
    for time in range(0, len(sound) - pieceTime, pieceTime):

        # time + pieceTime = ending time of piece
        piece = sound[time : time + pieceTime]

        # If at first element of pan array (Left) then iterate forward
        if panIndex == 0:
            iteratePanArrayForward = True

        # If at last element of pan array (Right) then iterate backward
        if panIndex == len(pan) - 1:
            iteratePanArrayForward = False

        # (panBoundary / 100) brings panBoundary to the same scale as elements of pan array i.e. -1.0 to 1.0
        # abs(pan[panIndex]) / (panBoundary / 100) = 1 for extreme left/right and 0 for center
        # abs(pan[panIndex]) / (panBoundary / 100) * volumeMultiplier = volumeMultiplier for extreme left/right and 0 for center
        # Hence, volAdjust = 0 for extreme left/right and volumeMultiplier for center
        volAdjust = volumeMultiplier - (
            abs(pan[panIndex]) / (panBoundary / 100) * volumeMultiplier
        )

        # Decrease piece volume by volAdjust i.e. max volume at extreme left/right and decreases towards center
        piece -= volAdjust

        # Pan the piece of sound according to the pan array element
        pannedPiece = piece.pan(pan[panIndex])

        # Iterates the pan array from left to right, then right to left, then left to right and so on..
        if iteratePanArrayForward:
            panIndex += 1
        else:
            panIndex -= 1

        # Add this panned piece of sound with adjusted volume to the 8d sound
        sound8d = sound8d + pannedPiece

    return sound8d
