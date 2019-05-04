import os
import nltk
import parse


def complete_sentence():
    cl = dict()
    sent = str()
    with open('./clause_output.txt', 'r') as f:
        for line in f.readlines():
            # print(line)
            if line.split(':')[0] == 'GIVEN SENTENCE':
                sent = line.split(':')[1].split('\"')[0].strip()
                print(sent)
            elif 'Clause' in line.split(':')[0]:
                key = line.split(':')[0].strip()[6]
                value = line.split(':')[1].strip()
                cl[key] = value

    parsed, tokens = parse.format(sent)
    triples = parsed.triples()
    conll = parsed.to_conll(10)
    dot = parsed.to_dot()
    for p in triples:
        print(listp)   
complete_sentence()