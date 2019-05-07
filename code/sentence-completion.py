import os
import nltk
import parse

def get_index(dict1, tree, w1, w2):
    l = []
    for k, v in dict1.items():
        if v == w1[0] and w1 in tree[w2]:
            l.append(k)
    if l == []:
        return 100000
    return l[0]

def complete_sentence():
    cl = dict()
    sent = str()
    clauserel = ['parataxis','ccomp','acl','acl:relcl','advcl','conj']

    with open('./clause_output.txt', 'r') as f:
        for line in f.readlines():
            # print(line)
            if line.split(':')[0] == 'GIVEN SENTENCE':
                sent = line.split(':')[1].split('\"')[0].strip()
            elif 'Clause' in line.split(':')[0]:
                key = line.split(':')[0].strip()[6]
                value = line.split(':')[1].strip()
                cl[key] = value
    print(sent)
    sentdict = {k:v for k, v in enumerate(sent.split( ))}
    parsed, tokens = parse.format(sent)
    input_tree = parsed.to_conll(4)
    ll = [line.split('\t')[1] for line in input_tree.split('\n') if line != '' and line.split('\t')[1] != 'POS']
    # print(ll)
    triples = parsed.triples()
    conll = parsed.to_conll(10)
    dot = parsed.to_dot()
    clause_marked = {}
    tree = {}
    for p in triples:
        # print(p)
        w1,rel,w2 = p
        if w1 not in tree:
            tree[w1] = {}
        if w2 not in tree[w1]:
            tree[w1][w2] = rel
        if rel in clauserel:
            clause_marked[rel] = p
    # print(clause_marked)
    # print(tree[('who', 'WP')])
    # print("TREE:")
    # for k in tree:
        # print(k, tree[k])
    # print("\n\n")
    clause_breakpoint = {}
    for k, v in clause_marked.items():
        # print("V: ",v)
        w1,rel,w2 = v
        nearest_noun_index = 100000
        if w2 not in tree:
            continue
        for w, crel in tree[w2].items():
            # print(w, w2 ,crel)
            if w[1][0] == 'N' or crel == 'nsubj' or crel == 'expl' or crel == 'advmod':
                temp = min(get_index(sentdict, tree, w, w2),get_index(sentdict, tree, w, w2))
                if temp < nearest_noun_index:
                    nearest_noun_index = temp
        # print(nearest_noun_index)
        # print(sentdict[nearest_noun_index])
        if nearest_noun_index == 100000:
            continue
        clause_breakpoint[v] = (nearest_noun_index, sentdict[nearest_noun_index])
    # print(clause_breakpoint)
    ln = [v[0] for v in clause_breakpoint.values()]
    ln = sorted(ln)
    xc = 1
    Sentences = {}
    for k, v in sorted(sentdict.items(),key = lambda x : x[0]):
        if k == ln[0]:
            xc += 1
        if ll[k] == 'CC' or ll[k] == 'WRB' or ll[k] == 'WDT':
            continue

        stored_p = ()
        stored_l = []
        # print(v)
        # if v == 'bought':
        for key in clause_breakpoint:
            # print(v, key[2][0], key[1])
            if v == key[2][0] and key[1] == 'acl:relcl':
                stored_p = key[0]
        # print(stored_p)
        if stored_p != ():
            for asd in tree[stored_p]:
                # print(asd)
                if asd[0] != v:
                    # print(asd)
                    stored_l.append(asd[0])
            # print(stored_l)
            stored_l.append(stored_p[0])
            v += ' '+ ' '.join(stored_l)
        cn = 'Clause'+str(xc)
        if cn not in Sentences:
            Sentences[cn] = ''
            v = v.capitalize()
        Sentences[cn] += v + ' '
    for k, v in Sentences.items():
        print(k,": ",v.strip() + '.')
complete_sentence()