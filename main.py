# used in conjunction with foo_np_simple
# with the formatting string set to: %path%
# only works with flac files (you could probably change that)

# put path to tracker file here \|/
trackerPath = r"C:\Users\Main\Documents\Temp\NP\nowPlaying.txt"

# value to assume if no replaygain information exists (the difference between the "With RG info" and "Without RG info):
withoutRGinfo = -10

# required libraries: comtypes, pycaw, mutagen

# 1.) scan all tracks with replaygain (make sure to scan tracks and not albums) (not *necessary if you set withoutRGinfo, though recommended)
# 2.) set your volume to your target (pivot) volume (I use 50%) then start the script
# 3.) while listening to music in foobar, adjust your windows volume and and the
# script will update the replaygain value after the music is finished

# will update the replaygain data of the previous track when you change tracks
# based on your windows volume

# MAKE SURE YOU HAVE SOURCE MODE IN THE PLAYBACK TAB SET TO 'TRACK', OTHERWISE YOU WILL NOT HEAR VOLUME THE SCRIPT THINKS YOU DO

import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


# Set baseVol to the pivot volume if you arent using different pivot volumes each time
baseVol = volume.GetMasterVolumeLevel()
oldGain = baseVol



print('pivot volume: ',baseVol)

from mutagen.flac import FLAC

with open(trackerPath, encoding='utf-8') as temp:
    prevPath = temp.read()
    temp.close()
count = 0
while True:
    # polling interval
    time.sleep(2)

    with open(trackerPath, encoding='utf-8') as temp:
        path = temp.read()
        temp.close()
    if path == 'not running' or path == 'n/a':
        print('|', '\n' * (count > 50), sep='', end='')
        count = (count < 50) * (count + 1)
        continue
    if path == prevPath:
        oldGain = volume.GetMasterVolumeLevel()
        print('.', '\n' * (count > 50), sep='', end='')
        count = (count < 50) * (count + 1)
        continue
    if prevPath == 'not running' or prevPath == 'n/a':
        prevPath = path
        continue
    flcF = FLAC(prevPath)
    print('\n',flcF['title'])
    try: currentReplayGain = flcF['replaygain_track_gain'][0][:-3]
    except:
        print('\n', 'no replaygain value found; assuming ', withoutRGinfo, 'dB', sep='')
        currentReplayGain = withoutRGinfo
    newReplayGain = (oldGain - baseVol) + float(currentReplayGain)
    print(round(float(currentReplayGain), 2), ' --> ', round(float(newReplayGain), 2), '   (difference of ', round(float(newReplayGain) - float(currentReplayGain), 2), 'dB)', sep='')
    flcF['replaygain_track_gain'] = str(str(newReplayGain) + ' dB')
    flcF['RGE'] = 'Edited'
    flcF.save()

    prevPath = path
    count = 0
    currentGain = volume.GetMasterVolumeLevel()
