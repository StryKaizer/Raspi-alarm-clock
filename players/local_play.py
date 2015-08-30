from subprocess import call
import random

music_folder = "/home/pi/music"


from os import listdir
from os.path import isfile, join
music_files = [ f for f in listdir(music_folder) if isfile(join(music_folder,f)) ]

random.shuffle(music_files)

for music_file in music_files:
    print "Now playing", music_file
    call(["omxplayer", music_folder + '/' + music_file])
