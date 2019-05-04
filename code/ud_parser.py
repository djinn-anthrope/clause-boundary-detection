import sys
import pickle
import parse

def get_dict(tree):
	dictList = {}
	depTree = {}
	dictList[0] = {'index':0,'word':'///root','root':None}
	for line in tree:
		if len(line) < 2:
			continue
		d = {'index':int(line[0]),
			 'word':line[1],
			 'rootword':line[2],
			 'cpos':line[3],
			 'pos':line[4],
			 'tam':line[5],
			 'root':int(line[6]),
			 'rel':line[7],
			 'rootrel':line[8],
			 'other':line[9]}
		dictList[d['index']] = d
		depTree[d['index']] = d['root']
	return dictList, depTree

def find_root(tree):
	for line in tree:
		if tree[line]['root'] == 0:
			return line
	return False	

ifile = open(sys.argv[1],'r')

trees = ifile.read().split("\n\n")
trees = [[line.split('\t') for line in tree.split('\n') if len(line) > 0] for tree in trees]

clauseProbs = []
verbList = ['V']
ignCount = 0
for tree in trees:
	vcount = 0
	for line in tree:
		# print(line)
		if line[0][0] == '#':
			continue
		# print(line[0])
		if '.' in line[0]:
			ignCount += 1
			vcount = 0
			break
		if line[3] == 'VERB':
			vcount += 1
	if vcount > 2:
		# print(tree)
		clauseProbs.append(tree)
print("Number of sentences with more than two clauses: ",len(clauseProbs))
print("Number of sentences ignored: ",ignCount)
print(clauseProbs[0])
input_sent = str(input("Input Sentence here --> "))

input_tree, tokens = parse.format(input_sent)
input_tree = input_tree.to_conll(10)
treeparsed = [line.split('\t') for line in input_tree.split('\n')]
if treeparsed[-1] == ['']:
	del treeparsed[-1]
print(treeparsed)
copy = treeparsed[:]
j = 0
for i, line in enumerate(treeparsed):
	print(i, line)
	if int(line[0]) == (i+j+1):
		continue
	else:
		print('i',i, j)
		if i + j < len(copy):
			copy.insert(i+j, [str(i+j+1),tokens[i+j],'_','PUNCT','PUNCT','_','-10000','_','_','_'])
		else:
			copy.append([str(i+j+1),tokens[i+j],'_','PUNCT','PUNCT','_','-10000','_','_','_'])
		j += 1
treeparsed = copy[:]
for line in treeparsed:
	print(line)

ofile = open('clause_data.pkl','wb')
o1file = open('clause-treebank.conllu','w')
o2file = open('clause_output.txt','w')
pickle.dump(clauseProbs,ofile)

for tree in clauseProbs:
	for line in tree:
		o1file.write("\t".join(line) + "\n")
	o1file.write("\n")
clauseProbs = [treeparsed]
# iter = 0
for tree in clauseProbs:
	# if iter >= 5:
		# break
	# print(tree)
	treeDict, depTree = get_dict(tree)
	# print(treeDict)
	# print(depTree)
	root = find_root(treeDict)
	# print(root)
	coverage = {}
	queue = [0]
	clauserel = ['parataxis','ccomp','acl','acl:relcl','advcl','conj']
	clauseDict = {}
	clause = []
	headofclause = [key  for (key, value) in depTree.items() if value == 0][0]
	nextclause = []
	_itr = 0
	sentence = '"'
	sentence += treeDict[1]['word']
	for ind in range(2,len(treeDict)):
		if ind not in treeDict:
			continue
		if treeDict[ind]['cpos'] == 'PUNCT':
			sentence += treeDict[ind]['word']
		else:
			sentence += ' ' + treeDict[ind]['word']
	o2file.write("GIVEN SENTENCE: "+ input_sent + '"\n')
	# print([treeDict[ind]['word'] for ind in range(len(treeDict))])
	while queue != [] or nextclause != []:
		if queue == []:
			queue = [nextclause[0]]
			newclause = []
			clause = sorted(clause)
			# for ind in clause:
			# 	if ind == 0:
			# 		continue
			# 	if (ind+1) in clause or (ind-1) in clause:
			# 		newclause.append(ind)
			# 	else:
			# 		coverage[ind] = 0
			x = headofclause
			while x in clause:
				if x == 0:
					break
				if treeDict[x]['cpos'] == 'PUNCT':
					break
				newclause = [x] + newclause
				coverage[x] = 1
				x -= 1

			x = headofclause + 1
			while x in clause:
				if treeDict[x]['cpos'] == 'PUNCT':
					break
				newclause.append(x)
				coverage[x] = 1
				x += 1

			clauseDict[_itr] = newclause
			_itr += 1
			# print(clause, newclause, nextclause)
			clause = []
			headofclause = nextclause.pop(0)

		parent = queue.pop(0)
		clause.append(parent)
		children = [key  for (key, value) in depTree.items() if value == parent]
		newchildren = children
		# print(children)
		for child in children:
			# print(child)
			# print(treeDict)
			# print(treeDict[child])
			if treeDict[child]['rel'] in clauserel and treeDict[child]['pos'][0] == 'V':
				nextclause.append(child)
				newchildren.remove(child)

		queue = newchildren + queue


	newclause = []

	x = headofclause
	while x in clause:
		newclause = [x] + newclause
		coverage[x] = 1
		x -= 1

	x = headofclause + 1
	while x in clause:
		newclause.append(x)
		coverage[x] = 1
		x += 1
	clause = sorted(clause)

	clauseDict[_itr] = newclause
	_itr = 0

	clause = []
	xin = [x for x in range (1,len(treeDict)) if x not in coverage.keys()]
	while xin != []:
		ind = xin.pop(0)
		for key, clause in sorted(clauseDict.items(), key=lambda x: x[1][-1]):
			if (ind+1 in clause or ind-1 in clause):
				clause.append(ind)
				clauseDict[key] = sorted(clause)
				coverage[ind] = 1
				break
		if ind not in coverage:
			xin = xin + [ind]

	# print(clauseDict)
	xi = 1
	for index, newclause in sorted(clauseDict.items(), key=lambda x: x[1][-1]):
		if newclause == []:
			continue
		wordclause = treeDict[newclause.pop(0)]['word']
		for ind in newclause:
			if ind not in treeDict:
				continue
			if treeDict[ind]['cpos'] == 'PUNCT':
				wordclause += treeDict[ind]['word']
			else:
				wordclause += ' ' + treeDict[ind]['word']
		o2file.write("Clause"+str(xi)+ ": "+ wordclause + "\n")
		xi += 1
		# print("\n\n")
	o2file.write("\n\n")
	# iter += 1
	# for line in tree: