from Utils import AD1HL, AD1HLUP, Check
import time
from random import randint

ad1hl = AD1HL()

check = Check()

songs = open("list_songs.txt", "r").read().splitlines()

for song in songs:
    if check.check(song) == False:
        a = ad1hl.make(song)

        uploader = AD1HLUP()

        uploader.upload(a["path"], a["title"], a["description"])

        time.sleep(randint(20, 60))
        