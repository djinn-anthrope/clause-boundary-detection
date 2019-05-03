from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

# cf = CanvasFrame()
# t = Tree.fromstring('(S (NP this tree) (VP (V is) (AdjP pretty)))')


def format(sentence):
    path_to_jar = '/home/alok/Open_Source/stanford-full/stanford-parser-full-2017-06-09/stanford-parser.jar'
    path_to_models_jar = '/home/alok/Open_Source/stanford-full/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'

    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
    tokens = word_tokenize(sentence)
    result = dependency_parser.raw_parse(sentence)

    for dep in result:
        print(dep.tree())
        cf = CanvasFrame()
        t = dep.tree()
        tc = TreeWidget(cf.canvas(),t)
        cf.add_widget(tc,10,10) # (10,10) offsets
        cf.print_to_file('tree.ps')
        cf.destroy()
        return(dep.to_conll(10), tokens)

    
# print(format(str(input()))[0]) 
