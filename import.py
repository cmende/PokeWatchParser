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


import csv
import sqlite3
from datetime import datetime

conn = sqlite3.connect('spawns.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS pokemon')
c.execute('DROP TABLE IF EXISTS spawnpoint')
c.execute('DROP TABLE IF EXISTS spawn')
c.execute('CREATE TABLE pokemon (pkmnid integer primary key, pkmnnameen text, pkmnnamede text)');
c.execute('CREATE TABLE spawnpoint (spptid integer primary key, spptlat numeric, spptlong numeric)');
c.execute('CREATE TABLE spawn (spwnid integer primary key, spwntime timestamp, spwnpkmnid integer, spwnspptid integer)');

# import pokemons
with open('pokemon.csv') as f:
    dr = csv.DictReader(f)
    values = [(row) for row in dr]
    c.executemany('INSERT INTO pokemon (pkmnid, pkmnnameen, pkmnnamede) VALUES (:pkmnid, :pkmnnameen, :pkmnnamede)', values)
    conn.commit()

# import spawns
with open('spawns.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        timestamp, pokemon, latitude, longitude = row

        # convert timestamp
        #2016-08-18 14:37:51
        datetime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

        # fetch pokemon id
        c.execute('SELECT pkmnid FROM pokemon WHERE pkmnnameen = ?', (pokemon,))
        pkmnid = c.fetchone()[0]

        # fetch gps id
        c.execute('SELECT spptid FROM spawnpoint WHERE spptlat = ? AND spptlong = ?', (latitude, longitude))
        result = c.fetchone()
        # new spawn point
        if result is None:
            c.execute('INSERT INTO spawnpoint (spptlat, spptlong) VALUES (?, ?)', (latitude, longitude))
            spptid = c.lastrowid
        # known spawn point
        else:
            spptid = result[0]

        # insert spawn
        c.execute('INSERT INTO spawn (spwntime, spwnpkmnid, spwnspptid) VALUES (?, ?, ?)', (datetime, pkmnid, spptid))

conn.commit()
conn.close()
