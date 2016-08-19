#!/usr/bin/env python3

# Copyright 2016 Christoph Mende
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import glob
from datetime import datetime, timedelta
import csv

csvwriter = None

def main():
    openCsv()
    files = glob.glob('*-log.txt')
    for file in files:
        if file == 'Launcher-log.txt' or file == 'Pokewatch-log.txt':
            continue
        parseFile(file)

def parseFile(filename):
    print('File: ' + filename)
    with open(filename) as f:
        for line in f:
            if "Tweeting" in line:
                parseLine(line.strip())

def openCsv():
    global csvwriter
    f = open('spawns.csv', 'w')
    csvwriter = csv.writer(f)

def parseLine(line):
    words = line.split(' ')

    # spawn timestamp
    #18.08.201606:38:13:
    spawned = datetime.strptime(words[0]+words[1], '%d.%m.%Y%H:%M:%S:')
    spawned -= timedelta(minutes=15)
    spawned += timedelta(seconds=int(words[4][1:]))

    # pokemon
    pokemon = words[3]
    
    # location
    location = words[6].replace(',', '.', 1).split(',', 1)
    latitude = float(location[0])
    longitude = float(location[1].replace(',', '.'))

    csvwriter.writerow((spawned, pokemon, latitude, longitude))

if __name__ == "__main__":
    main()
