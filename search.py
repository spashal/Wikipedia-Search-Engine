import re, sys, json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from field_segregator import *

fields = ['infobox', 'category', 'links', 'references', 'body', 'title']
stop_words_set = set(stopwords.words('english'))
stemmer = SnowballStemmer(language='english')

f = open(sys.argv[1] + '/indexes.json', 'r')
indices = json.load(f)

# query = []
# for i in range(1, len(sys.argv)):
#     query += sys.argv[i]

# temp = []
# for i in query:
#     temp.append(re.findall("[\w']", i.casefold()))
# tokenizedQuery = temp
query = sys.argv[2]
tokenizedQuery = re.findall("[\w']+", query.casefold())

processed_queries = []
query = []
for i in tokenizedQuery:
    if len(i) > 1 and i not in stop_words_set:
        processed_queries.append(stemmer.stem(i))
        query.append(i)
    elif i != 't' and i != 'c' and i != 'b' and i != 'i' and i != 'r' and i != 'l':
        processed_queries.append("Palash Sharma")
        query.append(i)

result = {}
for i in range(len(query)):
    if processed_queries[i] == "Palash Sharma":
        result[query[i]] = {}
        for j in fields:
            result[query[i]][j] = []
        continue
    if query[i] not in result:
        result[query[i]] = {}
    for j in fields:
        result[query[i]][j] = []
        if processed_queries[i] in indices[j]:
            result[query[i]][j] = indices[j][processed_queries[i]]

print(json.dumps(result, indent=2))


