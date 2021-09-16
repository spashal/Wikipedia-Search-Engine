import re, sys, json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from field_segregator import *

fields = ['infobox', 'category', 'links', 'references', 'body', 'title']
stop_words_set = set(stopwords.words('english'))
stemmer = SnowballStemmer(language='english')

# sys.argv[1] has path to index files
f = open('./palash/files_index.txt', 'r')
files_index = josn.load(f)

query = sys.argv[2]
check = re.split(':', query.casefold())
scores = {}
total_docs_global = 21300000

def give_scores(query, weights):
    # perform tf-idf on query 
    global scores, total_docs_global, files_index

    # find where the word is in indexes
    up = len(files_index)-1
    down = 0
    index = -1
    while up >= down:
        if files_index[up] < query:
            index = up
            break
        elif files_index[down] > query:
            index = down-1
            break
        mid = down + int((up-down)/2)
        if files_index[mid] == query:
            index = mid
            break
        elif files_index[mid] < query:
            low = mid
        else:
            up = mid-1
    
    # load that file as a json and get its posting list
    if index < 0:
        return -1
    f = open(sys.argv[1] + '/' + index + '-merged.txt', 'r')
    merged_index = json.load(f)
    if query not in merged_index:
        return -1
    postingList = merged_index[query]

    # convert posting list to readable and usable posting list
    posting_list_readable = {}
    sum = [0 for i in range(6)]
    tokens = re.split(' ', postingList)
    for i in tokens:
        doc = re.split('-', i)
        posting_list_readable[doc[0]] = {}
        for j in range(1, len(doc)):
            field = int(re.split('.', doc[j])[0]))
            freq = int(re.split('.', doc[j])[1])
            posting_list_readable[doc[0]][field] = freq
            # get sum of fieldwise frequencies
            sum[field] += 1

    # calculate idf fieldwise
    for i in range(6):
        idf.append(log(total_docs_global/sum[i]))

    # loop over all docs to calculate fieldwise scores also using weights for fields
    for i in posting_list_readable:
        for j in posting_list_readable[i]:
            scores[i] += log(1+posting_list_readable[i][j])*idf[j]*weights[j]    


processed_queries = []
query = []

# check if the query is field or plain
if len(check) == 1:
    # for plain query, fix the weights and send for scoring
    weights = [2.5, 3, 0.2, 0.8, 1, 5]
    
else:
    # for field query, flex the weights according to field and send for scoring

# after the getting the scores, select 10 docs and retrieve titles (make a separate function for this)

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


