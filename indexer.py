import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from field_segregator import *

fields = ['infobox', 'category', 'links', 'references', 'body', 'title']
stop_words_set = set(stopwords.words('english'))
stemmer = SnowballStemmer(language='english')

totalTokens = set()

def work_with_index_list(indices, id, field, curTokens, counter):
    # capturing the inverted index
    for i in range(len(curTokens)):
        counter += 1
        if len(curTokens[i]) > 15 or curTokens[i] == "":
            continue
        totalTokens.add(curTokens[i])
        if curTokens[i] not in indices:
            indices[curTokens[i]] = {}
            indices[curTokens[i]][id] = set()
            indices[curTokens[i]][id].add(field)
        else:
            if id not in indices[curTokens[i]]:
                indices[curTokens[i]][id] = set()
                indices[curTokens[i]][id].add(field)
            else:
                indices[curTokens[i]][id].add(field)
    return counter, indices

def add_to_index(text, id, indices, counter):
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
                temp.append(stemmer.stem(curTokens[i]))
        curTokens = temp

        # capturing the inverted index
        counter, indices = work_with_index_list(indices, id, j, curTokens, counter)
    
    return counter, indices
