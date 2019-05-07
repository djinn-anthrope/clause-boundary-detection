#Authors: Abheet Sharma(20161091) & Alok Debnath(20161122)

#English UD Data stats:
Tree count:  12543
Word count:  204607
Token count: 204607
Dep. relations: 378 of which 341 language specific
POS tags: 17
Category=value feature pairs: 37

There exists 3604 sentences with more than two clauses


#LINK TO DATA
https://drive.google.com/open?id=1MkTiNqoWWNTN2wcGc6zDS_uVtNtLV-Kf (clause-treebank.conllu or UD_English-EWT/en_ewt-ud-train.conllu is required)


#Relations
Types of clause relations:
- Parataxis: Phrases and clauses are placed one after another independently, without coordinating or subordinating them through the use of conjunctions.
- ccomp: A clausal complement of a verb or adjective is a dependent clause with an internal subject which functions like an object of the verb or adjective.
- acl: acl stands for finite and non-finite clauses that modify a nominal.
- acl:relcl: A relative clause modifier of an noun is a relative clause modifying the noun.
- advcl: An adverbial clause modifier is a clause which modifies a verb or other predicate (adjective, etc.), as a modifier not as a core complement.
- cc: A cc is the relation between a conjunct and a preceding coordinating conjunction. 


#FILES
DgAnnotator is used to visualize a dependancy tree from conllu data. This was used to identify patterns in clauses, their boundaries and their relations with other clauses.

parse.py takes in an input sentence, and returns it in conll format, which we can then parse. It also creates a tree.ps which displays the sentence in a dependancy tree format.

ud_parser.py does two thing
- creates a subfile 'clause-treebank.conllu' from the english treebank in which the sentences in clause-treebank contain more than two clauses(a corresponding pickle file is also created).
- Takes in input sentence from outside file. Uses parse.py to get conll type sentences and splits the sentences into clauses, thus identifying clause boundaries and writes it to 'clause_output.txt'.

sentence_completion.py takes in sentence, splits them and tries to complete the sentences to get readable individual sentences.


#HOW TO RUN
parse.py cannot be run on its own

to run ud_parser.py, do 'python3 ud_parser.py 'path to conll treebank' <  'path to textfile containing input sentence'
OR 'python3 ud_parser.py 'path to conll treebank'  and input the sentence when the prompt occurs

to run sentence_completion.py, first we need to run ud_parser.py to get clause_output.py, after that we run 'python3 sentence_completion.py'



