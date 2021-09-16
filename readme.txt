The python files I have made are :-
    1. field_segregator.py
    2. indexer.py
    3. merge.py
    4. parser.py
    5. search.py
    6. separate_titles.py

field_segregator:- Meant to take care of sperating tokens based on their fields and then returning the tokens made
indexer:- does the main task of indexing where it recieves the tokens from field_segregator and tasks like removing stopwords
          and stemming all happen here.
merge:- this file merges the indexes that have been separated on the basis of document count. Merging takes places 
        by merging all the index files at a time and simultaneously splitting the merged indexes in a sorted order
        of tokens so that file sizes remain manageable.
parser:- Used etree for parsing here. just basic parsing and also this is the main python function that is called
         while indexing the dump
search:- tf-idf search implemented here
separate_titles:- due to a small mistake in indexer, i had to split titles using a new script. the titles were originally
                  all output into a single big file
