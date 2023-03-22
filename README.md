# Automatic ReplayGain Adjustment From Windows Volume
  Automatically adjusts the replaygain value of the previously playing audio track based on a set pivot and your windows volume to allow for faster manual editing of replaygain values.

Used in conjunction with foo_np_simple with the formatting string set to: %path%

This currently only works with flac files (you could probably change that)

required libraries: comtypes, pycaw, mutagen

## Steps
1. Scan all tracks with replaygain (make sure to scan tracks and not albums) (not *necessary if you set withoutRGinfo, though recommended)
2. Set your volume to your target (pivot) volume (I use 50%) then start the script
3. While listening to music in foobar, adjust your windows volume and and the script will update the replaygain value after changing to the next track


# MAKE SURE YOU HAVE SOURCE MODE IN THE PLAYBACK TAB SET TO 'TRACK', OTHERWISE YOU WILL NOT HEAR VOLUME THE SCRIPT THINKS YOU DO
