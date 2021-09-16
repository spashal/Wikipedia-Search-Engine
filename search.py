import re, sys, json, math
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from field_segregator import *

fields = ['infobox', 'category', 'links', 'references', 'body', 'title']
field_symbols = {"i":1, "c":2, "l":3, "r":4, "b":5, "t":6}
stop_words_set = set(stopwords.words('english'))
stemmer = SnowballStemmer(language='english')

# sys.argv[1] has path to index files
f = open('./palash/files_index.txt', 'r')
ff = open('./palash/minId.txt', 'r')
first_id = int(ff.read())
files_index = json.load(f)

query = sys.argv[2]
check = re.split(':', query.casefold())
scores = {}
total_docs_global = 21300000

def get_title(doc_id):
    # print("getting title for", doc_id)
    global first_id
    file_no = int((int(doc_id)-first_id)/500000) + 1
    fil = open('./palash/' + str(file_no) + '-titles.txt', 'r')
    files = json.load(fil)
    if doc_id not in files:
        return "doc_title_not_found"
    return files[doc_id]

def give_scores(query, weights):
    # perform tf-idf on query 
    # print("making scores for", query)
    global scores, total_docs_global, files_index

    # find where the word is in indexes
    up = len(files_index)-1
    down = 0
    index = -1
    while up >= down:
        # print("here ", down, up)
        if files_index[up] <= query:
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
            down = mid
        else:
            up = mid-1
    
    # load that file as a json and get its posting list
    if index < 0:
        return -1
    index += 1
    print(query, " must be in ", index, "-merged.txt")
    f = open(sys.argv[1] + '/' + str(index) + '-merged.txt', 'r')
    merged_index = json.load(f)
    if query not in merged_index:
        return -1
    postingList = merged_index[query]

    # convert posting list to readable and usable posting list
    posting_list_readable = {}
    sum = [1 for i in range(6)]
    tokens = re.split(' ', postingList)
    for i in tokens:
        doc = re.split('-', i)
        posting_list_readable[doc[0]] = {}
        for j in range(1, len(doc)-1):
            temp = doc[j].split('.')
            field = int(temp[0])-1
            freq = int(temp[1])
            posting_list_readable[doc[0]][field] = freq
            # get sum of fieldwise frequencies
            sum[field] += 1

    idf = []

    # calculate idf fieldwise
    for i in range(6):
        idf.append(math.log(total_docs_global/sum[i]))

    # loop over all docs to calculate fieldwise scores also using weights for fields
    for i in posting_list_readable:
        for j in posting_list_readable[i]:
            if i not in scores:
                scores[i] = 0
            scores[i] += math.log(1+posting_list_readable[i][j])*idf[j]*weights[j]    


processed_queries = []
query = []
weights = [2.5, 3, 0.2, 0.8, 1, 5]

# check if the query is field or plain
if len(check) == 1:
    # for plain query, fix the weights and send for scoring
    tokenizedQuery = re.split(r'[^A-Za-z0-9]+', check[0])
    for i in tokenizedQuery:
        if len(i) > 1 and i not in stop_words_set:
            processed_queries.append(stemmer.stem(i))
            give_scores(i, weights)
else:
    symbol = re.split(r'[^A-Za-z0-9]+', check[0])[0]
    # for field query, flex the weights according to field and send for scoring
    for i in range(1, len(check)):
        temp_weights = weights.copy()
        # symbol = re.split(r'[^A-Za-z0-9]+', check[i])
        temp_weights[field_symbols[symbol]-1] = 10
        tokenizedQuery = re.split(r'[^A-Za-z0-9]+', check[i])
        for j in tokenizedQuery:
            if len(j) > 1 and j not in stop_words_set:
                processed_queries.append(stemmer.stem(j))
                give_scores(j, temp_weights)
        symbol = tokenizedQuery[-1]

# after the getting the scores, select 10 docs and retrieve titles (make a separate function for this)
sorted_docs = dict(sorted(scores.items(), key=lambda item: -item[1]))
result = ''
count = 0
for i in sorted_docs:
    count += 1
    result += i + ', '
    result += get_title(i) + '\n'
    if count > 10:
        break

print(result)
# f = open('./result.txt', 'w')
# f.write(result)
# f.close()

