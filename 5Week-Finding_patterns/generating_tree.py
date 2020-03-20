from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph

parser = CoreNLPDependencyParser(url='http://localhost:9000')

sentence = "Conan is running in the school"
parse, = parser.raw_parse(sentence)
conll = parse.to_conll(4)
print(conll)
dg = DependencyGraph(conll)
dotted = dg.to_dot()
G = dg.nx_graph()
f = open('test_'+str(datetime.now())+'.svg', 'w')
svg = dg._repr_svg_()
f.write(svg)
