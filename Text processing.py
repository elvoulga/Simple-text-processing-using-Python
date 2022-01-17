#!/usr/bin/env python
import sys
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import itertools

SYMBOLS = '!@#$%^&*()[]{};\':",.<>/?`~-_=+'

def extr_docs(cran_file):
    """Extract and return the Cranfield documents into a [(id,term)] form"""
    running_idx = -1
    in_text = False
    id_term_list = []
    for line in open(cran_file):
        if line.startswith('.I'):
            in_text = False
            running_idx = int(line.split()[1])
        else:
            if line.startswith('.W'):
                in_text = True
        if in_text:
            id_term_list += [(running_idx, t) for t in line.split()]
    return id_term_list

def main():
    # Get the cranfield collection filename as the 1st argument:
    if len(sys.argv) != 2:
        print 'Usage: textproc.py <Path to Cranfield collection>'
        sys.exit(1)
    cran_file = sys.argv[1]

    # Extract the documents in a convenient format:
    lst = extr_docs(cran_file)

    # Get list of stop-words and instantiate a stemmer:    
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    # Remove symbols:
    lst = [(x[0], ''.join([c if c not in SYMBOLS else '' for c in x[1]])) for
            x in lst]

    # Remove words <= 3 characters:
    lst = [x for x in lst if len(x[1]) > 3]

    # Remove stopwords:
    lst = [x for x in lst if x[1] not in stop_words]

    # Stem terms:
    lst = map(lambda x: (x[0], stemmer.stem(x[1])), lst)

    # Sort according to term:
    lst.sort(key=lambda x: x[1])

    for key, group in itertools.groupby(lst, key=lambda x: x[1]):
        uniq_doc_ids = set([x[0] for x in list(group)])
        s_uniq_doc_ids = sorted(uniq_doc_ids)
        print key, reduce(lambda a, b: str(a) + ' ' + str(b), s_uniq_doc_ids)

if __name__ == '__main__':
    main()
