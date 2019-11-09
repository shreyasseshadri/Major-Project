from tokenizer import tokenize, TOK

tokens = {}


tokens['network'] = ['socket', 'connect', 'listen']
tokens['compute'] = ['for', 'while']
tokens['memory'] = ['list', 'import']

count_token = {k: 0 for k in tokens}
type_words = {k: set() for k in tokens}

# set()
lines = []
with open('sample.py', 'r') as f:
    for line in f.readlines():
        line = line.replace('\n', '').replace('\t', '')
        # print(line)
        lines.append(line)

for line in lines:
    for token in tokenize(line):
        # print(u"{0}: '{1}' {2}".format(
        #     TOK.descr[token.kind],
        #     token.txt or "-",
        #     token.val or ""))
        # print(five_tuple)
        # print(five_tuple.type)
        # print(five_tuple.string)
        # print(five_tuple.start)
        # print(five_tuple.end)
        # print(five_tuple.line)

        for t in count_token:
            if token.txt in tokens[t]:
                count_token[t]+=1
                type_words[t].add(token.txt)

print(count_token, type_words)
