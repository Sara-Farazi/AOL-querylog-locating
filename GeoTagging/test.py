import os
import pdb
import sqlite3
from nltk.tag import StanfordNERTagger


conn = sqlite3.connect("sample.db")
geonames_conn = sqlite3.connect("geonames.db")

curs = conn.cursor()
geonames_curs = geonames_conn.cursor()

ids = curs.execute("select distinct id from qlog").fetchall();


os.environ['CLASSPATH'] = "/home/sara/Desktop/AOLQueryLog/GeoTagging/stanford-ner-2016-10-31"
st = StanfordNERTagger('/home/sara/Desktop/AOLQueryLog/GeoTagging/stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz')

punctuations = ["'", '"', ":", ";", "-", "_", ")", "(", "[", "]", "{", "}", "’", "."]


for id_item in ids[1:]:
	id = id_item[0]
	queries = curs.execute("select query from qlog where id={}".format(id)).fetchall()

	print("Checking {} queries from id {}".format(len(queries), id))

	queries = ["I live in Edmonton.", ]

	for query in queries:
		annotated = st.tag(query.split())
		print("Query: {}, annotated: {}".format(query, annotated))
		for item in annotated: 
			if item[1] == 'LOCATION':

				item_name = item[0]

				for punct in punctuations: 
					item_name = item_name.replace(punct, "")


				quer = "select lat, long from geoname where name='{}' or ascii_name='{}' or altnames like '%{}%'".\
					format(item_name, item_name, item_name)

				print(quer)

				matches = geonames_curs.execute(quer).fetchall()

				pdb.set_trace()
