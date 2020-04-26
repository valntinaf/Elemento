import re
from elemento.relations import *
from elemento.time import Time
from elemento.inspector import Inspector
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph

parser = CoreNLPDependencyParser(url='http://localhost:9000')

def get_words( node, dg, filter=None):
    words = []
    for k, v in dg.nodes.get(node)['deps'].items():
        if filter:
            if not k in filter:
                words.extend(get_words(v[0], dg, filter))
        else:
            words.append(get_words(v[0], dg))
    words.append(dg.nodes.get(node)['word'])
    return words

def process_time( node, dg ):

    MOMENT = Time()
    SECOND = Time('55??', keywords=['second'])
    MINUTE = Time('55????', keywords=['minute'])
    HOUR = Time('55??????', keywords=['hour'])
    MORNING = Time('01????????', keywords=['morning'])
    AFTERNOON = Time('02????????', keywords=['afternoon'])
    EVENING = Time('03????????', keywords=['evening'])
    NIGHT = Time('04????????', keywords=['night'])
    DAY = Time('55??????????', keywords=['day'])
    words = get_words(node, dg, filter=['det'])
    time = Time()
    return MOMENT

class Notion:
    idees = []

    def __init__(self):
        matchers = []
        f = open("/home/vale/Projects/elemento/elemento/patterns.pt","r+")
        for line in f.readlines():
            result = {}
            pattern = line.split(' ')
            wfp = re.findall(r"[\w:']+", pattern[0])
            wfp.reverse()
            wtm = re.findall(r"[\w']+", pattern[1])
            wtm.reverse()

            relations = []
            parent = None

            deep = 0

            pattern[0]+="."
            for c in pattern[0]:
                if c == '{':
                    deep+=1
                    if deep == 2:
                        if not parent:
                            relations.pop()
                            parent = f

                    a = wtm.pop()
                    b = wfp.pop()

                    if b.isupper():
                        f = MATCH_TAG(a, b)
                    else:
                        f = MATCH_REL(a, b)
                    if parent:
                        f = SON_F(f,1)

                    relations.append(f)
                if c == '}':
                    deep-=1
                    if deep == 0:
                        f = relations.pop()
                        while relations:
                            f = AND_F(f, relations.pop())
                        f = AND_F(parent, f)
                        parent = f

                    if not relations:
                        parent = SON_F(f,-1)

            result = parent
            matcher = result
            matchers.append(matcher)
        self.matchers = matchers

    def process_text( self, text):
        sequencial_time = 0
        now = Time()
        for sentence in text:
            parse, = parser.raw_parse(sentence)
            conll = parse.to_conll(4)
            print(conll)
            dg = DependencyGraph(conll)
            i = Inspector( dg.nodes )
            for matcher in self.matchers:
                idee = matcher(i)
                if idee:
                    idee.dg = dg
                    if not idee.dictionary.get('WHEN', False):
                        now = now + now
                        idee.time = now
                    else:
                        idee.time =  process_time( idee.dictionary['WHEN'], dg)
                    self.idees.append(idee)
                    sequencial_time += 1

    def process_sentence(self, sentence):
        parse, = parser.raw_parse(sentence)
        conll = parse.to_conll(4)
        dg = DependencyGraph(conll)
        i = Inspector( dg.nodes )
        for matcher in self.matchers:
            idee = matcher(i)
            if idee:
                idee.dg = dg
                self.idees.append(idee)