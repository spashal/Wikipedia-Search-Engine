import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from field_segregator import *

fields = ['infobox', 'category', 'links', 'references', 'body', 'title']
stop_words_set = set(stopwords.words('english'))
stemmer = SnowballStemmer(language='english')

totalTokens = set()
stemmed = {}

def work_with_index_list(indices, id, field, curTokens, counter):
    # capturing the inverted index
    for i in range(len(curTokens)):
        counter += 1
        if len(curTokens[i]) > 15 or curTokens[i] == "":
            continue
        totalTokens.add(curTokens[i])
        if curTokens[i] not in indices:
            indices[curTokens[i]] = {}
            indices[curTokens[i]][id] = [0 for i in range(6)]
            indices[curTokens[i]][id][field] += 1
        else:
            if id not in indices[curTokens[i]]:
                indices[curTokens[i]][id] = [0 for i in range(6)]
                indices[curTokens[i]][id][field] += 1
            else:
                indices[curTokens[i]][id][field] += 1
    return counter, indices

def add_to_index(text, id, indices, counter):
    global stemmed

    field = 'title'        # for testing purposes
    # tokenization 
    if text == None:
        return counter, indices
    tokens = field_segregator(text)

    for j in range(5):
        curTokens = tokens[fields[j]]
        # case folding
        for i in range(len(curTokens)):
            curTokens[i] = curTokens[i].casefold()

        # removing stop words and stemming them at the same time
        temp = []
        for i in range(len(curTokens)):
            if curTokens[i] not in stop_words_set:
                if curTokens[i] not in stemmed:
                    stemmed[curTokens[i]] = stemmer.stem(curTokens[i])
                temp.append(stemmed[curTokens[i]])
                if len(stemmed) > 10000000:
                    stemmed = {}
        curTokens = temp

        # capturing the inverted index
        counter, indices = work_with_index_list(indices, id, j, curTokens, counter)
    
    return counter, indices
