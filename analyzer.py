from tokenizer import tokenize, TOK
import os
from os import listdir
from os.path import isfile, join

tokens = {}
output_file = open('output.txt','w')


tokens['network'] = ['socket.socket', 'connect', 'listen']
tokens['compute'] = ['for', 'while']
tokens['memory'] = ['import']

PUNCTUATION = TOK.descr[TOK.PUNCTUATION]
NUMBER = TOK.descr[TOK.NUMBER]


def generate_token(file_name):
    lines = []
    with open(file_name, 'r') as f:
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
    return file_token


def get_file_tokens(directory):
    file_names = [os.path.join(directory, f) for f in listdir(
        directory) if isfile(join(directory, f))]
    file_tokens = {file_name: generate_token(
        file_name) for file_name in file_names}
    return file_tokens


file_tokens = get_file_tokens('programs')


def compute_score(file_token):
    total_tokens = 0
    mem_status, mem_tokens, _ = memory(file_token)
    if mem_status:
        total_tokens += mem_tokens

    com_status, com_tokens = compute(file_token)
    if com_status:
        total_tokens += com_tokens

    net_status, net_tokens = network(file_token)
    if net_status:
        total_tokens += net_tokens

    mem_score = mem_tokens / total_tokens
    com_score = com_tokens / total_tokens
    net_score = net_tokens / total_tokens

    # print("Memory score : ", mem_score, "\n", "Compute score : ",
    #       com_score, "\n", "Network score : ", net_score, "\n")
    return mem_score, com_score, net_score, mem_tokens, com_tokens, net_tokens


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
        index += 1
        if token[0] == PUNCTUATION and token[1] == '[':
            start_index = index
            flag = True
        if token[0] == PUNCTUATION and token[1] == ']' and index > start_index:
            return True, elem_count+1 if elem_count > 0 else 0
        if token[0] == PUNCTUATION and token[1] == ',' and index > start_index and flag:
            elem_count += 1
    return False, 0


def range_finder(line_token):
    flag = False
    index = 0
    for token in line_token[:-1]:
        index += 1
        if token[1] == 'range':
            flag = True
        if token[0] == NUMBER and flag:
            return True, token[1]
    return False, 0


def memory(file_token):
    list_tokens = 0
    list_types = []
    for line in file_token:
        isList, length = list_finder(line)
        if isList and length == 0:
            isList, length = range_finder(line)
        if isList:
            list_tokens += int(length)
            sent = line[-1]
            info_index = sent.find('#TOK')
            if info_index >= 0:
                list_types.append((length, sent[info_index:].split(' ')[1]))
    return (True, list_tokens, list_types)if list_tokens > 0 else (False, list_tokens, list_types)


def compute(file_token):
    iteration_count = 0
    for line in file_token:
        sent = line[-1]
        for_index = sent.find('for')
        if for_index >= 0:
            is_for, for_count = range_finder(line)
            if is_for:
                iteration_count += int(for_count)
    return (False, iteration_count) if iteration_count == 0 else (True, iteration_count)


def network(file_token):
    network_count = 0
    for line in file_token:
        sent = line[-1]
        connect_index = sent.find('.connect')
        listen_index = sent.find('.listen')
        send_index = sent.find('.send')
        if connect_index > 0:
            network_count += 1
        if listen_index > 0:
            network_count += 1
        if send_index > 0:
            offset = len(sent[send_index+5:])-4
            network_count += 1
            network_count += offset/100

    return (False, network_count) if network_count == 0 else (True, network_count)

def sprint(string):
    print(string)
    output_file.write(string)
    output_file.write("\n")

if __name__ == "__main__":
    total_mem_token = 0
    total_com_token = 0
    total_net_token = 0

    file_scores = []
    for file in file_tokens:
        sprint(" File name : " + file.split('/')[1])
        mem_score, com_score, net_score, mem_tokens, com_tokens, net_tokens = compute_score(
            file_tokens[file])
        total_com_token += mem_tokens
        total_mem_token += mem_tokens
        total_net_token += net_tokens

        sprint('')
        sprint('Memory Tokens  : ' + str(mem_tokens))
        sprint('compute Tokens : ' + str(com_tokens))
        sprint('network Tokens : ' + str(net_tokens))
        sprint('')

        sprint('Memory Score  : ' + str(mem_score))
        sprint('compute Score : ' + str(com_score))
        sprint('network Score : ' + str(net_score))
        sprint('')

        file_scores.append((file.split('/')[1],mem_score,com_score,net_score))
        sprint('='*90)

    
    sprint("Memory priority order ")
    for score in sorted(file_scores,key= lambda x: x[1],reverse=True):
        sprint('File name: ' + score[0] + " score : " + str(score[1]))

    sprint('')
    sprint("Compute priority order ")
    for score in sorted(file_scores,key= lambda x: x[2],reverse=True):
        sprint('File name: ' + score[0] + " score : " + str(score[2]))

    sprint('')
    sprint("Network priority order ")
    for score in sorted(file_scores,key= lambda x: x[3],reverse=True):
        sprint('File name: ' + score[0] + " score : " + str(score[3]))

    output_file.close()