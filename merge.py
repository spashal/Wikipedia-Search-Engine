import sys, os, heapq, json

files_index = []

def merger(no_of_files, path):
    global files_index
    k = no_of_files
    pq = []
    count_merged_files = 0
    tokensCount = 0
    # get pointers to all k files
    for i in range(1, k+1):
        name = path + '/' + str(i) + '.txt'
        f_ptr = open(name, 'r')
        line = f_ptr.readline().strip('\n')
        word = line.split(':')[0]
        lst = line.split(':')[1]
        pq.append((word, i, f_ptr, lst))

    # maintain a min heap of keys for each k files, their pointers and their  file numbers
    # (this will be useful while deciding which file to process first when they have the same key)
    heapq.heapify(pq)

    # maintain a new merged index where we will append the keys
    merged_index = {}

    # run a while loop in heap where we remove the topmost element each time and append to merged index
    while len(pq) > 0:
        cur = heapq.heappop(pq)
        if cur[0] in merged_index:
            merged_index[cur[0]] += str(cur[3])
            line = cur[2].readline().strip('\n')
            
            if line:
                word = line.split(':')[0]
                lst = line.split(':')[1]
                heapq.heappush(pq, (word, cur[1], cur[2], lst))
            else:
                cur[2].close()
                os.remove(path + '/' + str(cur[1]) + '.txt')
        # when we reach our limit of tokens and each token is complete in iteself, we can make a new file, write this file name and word in another file index
        elif sys.getsizeof(merged_index) > 512*1024:
            count_merged_files += 1
            for i in merged_index:
                files_index.append(i)
                break
            json_dump = json.dumps(merged_index,indent=0)
            f = open(path + '/' + str(count_merged_files) + '-merged' + '.txt', 'w')
            f.write(json_dump)
            f.close()
            merged_index = {}         # re-initializing the indices dictionary
            tokensCount = 1
            merged_index[cur[0]] = str(cur[3])
            line = cur[2].readline().strip('\n')
           
            if line:
                word = line.split(':')[0]
                lst = line.split(':')[1]
                heapq.heappush(pq, (word, cur[1], cur[2], lst))
            else:
                cur[2].close()
                os.remove(path + '/' + str(cur[1]) + '.txt')
        else:
            tokensCount += 1
            merged_index[cur[0]] = str(cur[3])
            line = cur[2].readline().strip('\n')
            if line:
                word = line.split(':')[0]
                lst = line.split(':')[1]
                heapq.heappush(pq, (word, cur[1], cur[2], lst))
            else:
                cur[2].close()
                os.remove(path + '/' + str(cur[1]) + '.txt')
        
        # continue until all the files have been merged

    # write into file one last time before we exit the function          
    count_merged_files += 1
    for i in merged_index:
        files_index.append(i)
        break
    json_dump = json.dumps(merged_index,indent=0)
    f = open(path + '/' + str(count_merged_files) + '-merged' + '.txt', 'w')
    f.write(json_dump)
    f.close()

    f = open(path + '/files_index.txt', 'w')
    f.write(json.dumps(files_index))
    f.close()

merger(6, './index')
