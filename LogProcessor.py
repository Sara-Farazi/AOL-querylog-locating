import os
import pdb
import sqlite3

directory = 'data/'

punctuations = ["'", '"', ":", ";", "-", "_", ")", "(", "[", "]", "{", "}"]

conn = sqlite3.connect("data/query.db")
curs = conn.cursor()
curs.execute("create table qlog(id integer, query text, time text)")
conn.commit()

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(directory + filename) as f:
            for line in f:
                parts = line.split("\t")
                entry = {
                    "id": parts[0],
                    "query": parts[1],
                    "time": parts[2],
                }

                
                for item in punctuations:
                    if item in parts[1]:
                        parts[1] = parts[1].replace(item, "")



                quer = "insert into qlog values('{}','{}','{}')".format(parts[0], parts[1], parts[2])   
                # print(quer)
                curs.execute(quer)

conn.commit()