import xml.etree.ElementTree as etree
import codecs, csv, time, os, json, sys
from indexer import *

# just some paths and names
OUT_PATH = '/Users/macbook/forgit/IRE/temp/Wikipedia-Search-Engine/dump'
DUMP_FILE = 'temp_data.xml'
ARTICLES = 'articles.csv'
REDIRECT = 'articles_redirect.csv'
TEMPLATE = 'articles_template.csv'
ENCODING = 'utf-8'

def time_as_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

pathWikiXML = sys.argv[1]
pathArticles = os.path.join(OUT_PATH, ARTICLES)
pathArticlesRedirect = os.path.join(OUT_PATH, REDIRECT)
pathTemplateRedirect = os.path.join(OUT_PATH, TEMPLATE)

counter = 0
totalCount = 0
articleCount = 0
redirectCount = 0
templateCount = 0
start_time = time.time()
indices = {}         # this is the inverted index
fields = ['infobox', 'category', 'links', 'references', 'body', 'title']

for i in range(6):
    indices[fields[i]] = {}

with codecs.open(pathArticles, "w", ENCODING) as articlesFH, \
        codecs.open(pathArticlesRedirect, "w", ENCODING) as redirectFH, \
        codecs.open(pathTemplateRedirect, "w", ENCODING) as templateFH:
    articlesWriter = csv.writer(articlesFH, quoting=csv.QUOTE_MINIMAL)
    redirectWriter = csv.writer(redirectFH, quoting=csv.QUOTE_MINIMAL)
    templateWriter = csv.writer(templateFH, quoting=csv.QUOTE_MINIMAL)

    articlesWriter.writerow(['id', 'title', 'redirect'])
    redirectWriter.writerow(['id', 'title', 'redirect'])
    templateWriter.writerow(['id', 'title'])
    
    for event, elem in etree.iterparse(pathWikiXML, events=('start', 'end')):
        tname = strip_tag_name(elem.tag)

        if event == 'start':
            if tname == 'page':
                title = ''
                id = -1
                redirect = ''
                inrevision = False
                ns = 0
            elif tname == 'revision':
                # Do not pick up on revision id's
                inrevision = True
            elif tname == 'title':
                    title = elem.text

            elif tname == 'id' and not inrevision and elem.text!=None:
                id = int(elem.text)
                if title == None:
                    continue
                title = title.casefold()
                curTokens = re.findall("[\w']+", title)
                temp = []
                for i in range(len(curTokens)):
                    if curTokens[i] not in stop_words_set:
                        temp.append(stemmer.stem(curTokens[i]))
                curTokens = temp
                # print(curTokens)
                counter, indices = work_with_index_list(indices, id, 'title', curTokens, counter)
            elif tname == 'redirect':
                redirect = elem.get('title', '')
            elif tname == 'ns' and elem.text!=None:
                ns = int(elem.text)
            elif tname == 'text':
                if id == -1:
                    continue
                counter, indices = add_to_index(elem.text, id, indices, counter)

        elif tname == 'page':
            totalCount += 1
            if ns == 10:
                templateCount += 1
            elif len(redirect) > 0:
                articleCount += 1
            else:
                redirectCount += 1

            if totalCount > 1 and (totalCount % 100000) == 0:
                continue

        elem.clear()
        
time_took = time.time() - start_time
count = 0
for i in indices:
    temp = {}
    for j in indices[i]:
        temp[j] = list(indices[i][j])
    indices[i] = temp

json_dump = json.dumps(indices, indent=2)
f = open(sys.argv[2], 'w')
f.write(json_dump)
f.close()


f = open(sys.argv[3], 'w')
f.write(str(counter) + '\n')
f.write(str(len(totalTokens)))
f.close()
