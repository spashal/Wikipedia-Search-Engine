import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from field_segregator import *

fields = ['infobox', 'category', 'links', 'references', 'body', 'title']
stop_words_set = set(stopwords.words('english'))
stemmer = SnowballStemmer(language='english')

def work_with_index_list(indices, id, field, curTokens):
    # capturing the inverted index
    for i in range(len(curTokens)):
        if curTokens[i] in indices[field]:
            indices[field][curTokens[i]].add(id)
        else:
            indices[field][curTokens[i]] = set()
            indices[field][curTokens[i]].add(id)
    return indices

def add_to_index(text, id, indices):
    field = 'title'        # for testing purposes
    # tokenization 
    if text == None:
        return indices
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
        indices = work_with_index_list(indices, id, fields[j], curTokens)
    
    return indices
