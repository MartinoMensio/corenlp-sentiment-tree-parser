from lark.lark import Lark
from lark.visitors import Transformer

parser = Lark.open('parser.lark', rel_to=__file__)

class SentimentTransformer(Transformer):
    # one method for each symbol defined and used
    # terminals
    NUMBER = float
    INT = int
    def WORD(self, args):
        return str(args)
    def LABEL(self, args):
        return str(args)
    # just propagation of child value
    def sentiment(self, args):
        assert isinstance(args[0], int)
        return args[0]
    def prob(self, args):
        return args[0]
    def target(self, args):
        return args[0]
    def expression(self, args):
        # print('expression', len(args), args)
        if isinstance(args[3], str):
            # assigned to word
            terminal = True
        else:
            # return list from subtree
            terminal = False
        return [{
            'constituent': args[0],
            'sentiment': args[1],
            'prob': args[2],
            'target': args[3],
            'terminal': terminal
        }]
            # to return also a subtree: 'target': set(w for el in args[3] for w in el['target'])
    def expression_list(self, args):
        # print('expression_list', args)
        if len(args) == 1:
            # only one expression (terminal)
            return args[0]
        else:
            # expression expression_list
            return args[0] + args[1]
    def start(self, args):
        # print('result', args[0])
        return args[0]
        


def parse_sentiment_string(sentiment_string: str):
    """Parse a string from CoreNLP sentimentTree property and return a tree"""
    tree = parser.parse(sentiment_string)
    # visit and perform transformation to desired output, also visit terminals
    result = SentimentTransformer(visit_tokens=True).transform(tree)
    return result

def d3_visit_node(node):
    # generate treeData variable for d3.js
    if isinstance(node, list):
        # root
        return [d3_visit_node(el) for el in node]
    result = {
        'name': '',
        # reds to blues
        'color': ['#ff0000', '#ff6e6e', '#ffffff', '#6e6eff', '#0000fc'][node['sentiment']],
        'label': ['--', '-', '0', '+', '++'][node['sentiment']]
    }
    if node['terminal']:
        # show text of the token
        result['name'] = node['target']
    else:
        result['children'] = [d3_visit_node(el) for el in node['target']]
    return result
