import os, sys, json

f = open('index/1-titles.txt', 'r')
titles = json.load(f)
f.close()

doc_count = 1
new_doc = {}
for title in titles:
    new_doc[title] = titles[title]
    if len(new_doc) == 50000:
        f = open('index/' + str(doc_count) + '-titles.txt', 'w')
        f.write(json.dumps(new_doc))
        f.close()
        new_doc = {}
        doc_count += 1

if len(new_doc) > 0:
    f = open('index/' + str(doc_count) + '-titles.txt', 'w')
    f.write(json.dumps(new_doc))
    f.close()
    new_doc = {}