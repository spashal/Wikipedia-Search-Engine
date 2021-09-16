import os, sys, json

titles_index = {}

for i in range(1, 428):
    f = open('./palash/' + str(i) + '-titles.txt', 'r')
    temp = json.load(f)
    for j in temp:
        titles_index[i] = int(j)
        break
    f.close()

f = open('./palash/titles_index.txt', 'w')
f.write(json.dumps(titles_index))
f.close()