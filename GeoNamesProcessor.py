import os
import pdb
import sqlite3

directory = 'data/'
filename = 'allCountries.txt'


conn = sqlite3.connect("data/geonames.db")
curs = conn.cursor()
curs.execute("create table geoname(id integer, name text, ascii_name text, altnames text, lat real, long real, population integer)")
conn.commit()

counter = 0

punctuations = ["'", '"', ":", ";", "-", "_", ")", "(", "[", "]", "{", "}", "’"]

with open(directory + filename) as f:
    for line in f:
        counter += 1
        parts = line.split("\t")

        for item in punctuations: 
        	parts[1] = parts[1].replace(item, "")
        	parts[2] = parts[2].replace(item, "")
        	parts[3] = parts[3].replace(item, "")


        quer = "insert into geoname values({},'{}','{}', '{}','{}', '{}', {})".format(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[14])   
        curs.execute(quer)

        if counter % 10000 == 0: 
        	print("Inserted {} items so far...".format(counter))

conn.commit()

