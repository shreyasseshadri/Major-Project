from tokenizer import tokenize, TOK

tokens = {}


tokens['network'] = ['socket', 'connect', 'listen']
tokens['compute'] = ['for', 'while']
tokens['memory'] = ['list', 'import']

count_token = {k: 0 for k in tokens}
type_words = {k: set() for k in tokens}

lines = []
with open('sample.py', 'r') as f:
    for line in f.readlines():
        line = line.replace('\n', '').replace('\t', '')
        # print(line)
        lines.append(line)

file_token = []
for line in lines:
    line_token = []
    for token in tokenize(line):
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
        if token[0] == TOK.descr[TOK.PUNCTUATION] and token[1] == '[':
            start_index = index
            flag = True
            # print(index)
        if token[0] == TOK.descr[TOK.PUNCTUATION] and token[1] == ']' and index > start_index:
            # print(index)
            return True, elem_count+1 if elem_count>0 else 0
        if token[0] == TOK.descr[TOK.PUNCTUATION] and token[1] == ',' and index > start_index and flag:
            elem_count += 1
            # print("comma ",index)


print(list_finder(file_token[-1]))
# print(file_token)
