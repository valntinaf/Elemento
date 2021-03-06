from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
import sys
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')

def parse(sentence,file=None):
    parse, = dep_parser.raw_parse(sentence)
    conll = parse.to_conll(4)
    cont = 0
    for line in conll.split('\n'):
        print(f'{cont}:\t{line} ')
        cont+= 1
    if file:
        f = open(file+'.svg', 'w')
        svg = parse._repr_svg_()
        f.write(svg)
        f.close()
    print(parse.to_conll(4))
    return parse