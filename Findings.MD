#Authors: Abheet Sharma(20161091) & Alok Debnath(20161122)

#English UD Data stats:
Tree count:  12543
Word count:  204607
Token count: 204607
Dep. relations: 378 of which 341 language specific
POS tags: 17
Category=value feature pairs: 37

There exists 3604 sentences with more than two clauses

Types of clause relations:
- Parataxis: Phrases and clauses are placed one after another independently, without coordinating or subordinating them through the use of conjunctions.
- ccomp: A clausal complement of a verb or adjective is a dependent clause with an internal subject which functions like an object of the verb or adjective.
- acl: acl stands for finite and non-finite clauses that modify a nominal.
- acl:relcl: A relative clause modifier of an noun is a relative clause modifying the noun.
- advcl: An adverbial clause modifier is a clause which modifies a verb or other predicate (adjective, etc.), as a modifier not as a core complement.
- cc: A cc is the relation between a conjunct and a preceding coordinating conjunction. 
- xcomp: An open clausal complement (xcomp) of a verb or an adjective is a predicative or clausal complement without its own subject.

DgAnnotator is used to visualize a dependancy tree from conllu data. This was used to identify patterns in clauses, their boundaries and their relations with other clauses.

ud_parser.py does two things
- creates a subfile 'clause-treebank.conllu' from the english treebank in which the sentences in clause-treebank contain more than two clauses(a corresponding pickle file is also created).
- parses conllu type sentences and splits the sentences into clauses, thus identifying clause boundaries and writes it to 'clause_output.txt'.



