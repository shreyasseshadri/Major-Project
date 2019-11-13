from tokenizer import tokenize, TOK

tokens = {}


tokens['network'] = ['socket.socket', 'connect', 'listen']
tokens['compute'] = ['for', 'while']
tokens['memory'] = ['list', 'import']

PUNCTUATION = TOK.descr[TOK.PUNCTUATION]
NUMBER  = TOK.descr[TOK.NUMBER]

count_token = {k: 0 for k in tokens}
type_words = {k: set() for k in tokens}

lines = []
with open('sample.py', 'r') as f:
    for line in f.readlines():
        line = line.replace('\n', '').replace('\t', '')
        lines.append(line)

file_token = []
for line in lines:
    line_token = []
    comment = False
    for token in tokenize(line):
        if token.txt == "#":
            comment = True
        if comment and token.txt != "TOK":
            comment = False
            break
        line_token.append(
            (TOK.descr[token.kind], token.txt or None, token.val or None))

    line_token.append(line)
    file_token.append(line_token)


def list_finder(line_token):
    sent = line_token[-1]
    first = sent.find('[')
    last = sent.find('[')
    if first != -1:
        if last > first:
            pass

    start_index = -1
    elem_count = 0
    index = -1
    flag = False
    for token in line_token[:-1]:
        # print(token)
        index += 1
        if token[0] == PUNCTUATION and token[1] == '[':
            start_index = index
            flag = True
            # print(index)
        if token[0] == PUNCTUATION and token[1] == ']' and index > start_index:
            # print(index)
            return True, elem_count+1 if elem_count>0 else 0
        if token[0] == PUNCTUATION and token[1] == ',' and index > start_index and flag:
            elem_count += 1
            # print("comma ",index)
    return False,0

def list_range_finder(line_token):
    flag = False
    index = 0 
    for token in line_token[:-1]:
        index+=1
        if token[1] == 'range':
            flag =True
        if token[0] == NUMBER and flag:
            return True,token[1]
    return False,0


for line in file_token:
    isList,length = list_finder(line)
    if isList and length == 0:
        isList, length = list_range_finder(line)
    if isList:
        print(isList , length)

print(file_token)