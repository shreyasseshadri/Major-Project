utilization = {}
utilization['network'] = []
utilization['memory'] = []
utilization['compute'] = []

network_format = """
unix timestamp;iface_name;bytes_out/s;bytes_in/s;bytes_total/s;bytes_in;bytes_out;packets_out/s;packets_in/s;packets_total/s;packets_in;packets_out;errors_out/s;errors_in/s;errors_in;errors_out
"""


def get_network_info(line, column_name):
    index = network_format.split(';').index(column_name)
    return ('' if index < 0 else line.split(';')[index])


def read_vm_characteristics(util_file):
    comp_avg = 0
    mem_avg = 0
    with open(util_file, 'r') as f:
        for ind, line in enumerate(f.readlines()[:9]):
            line = line.replace('\n', '').replace('\t', '').replace(
                ' ', '').replace('total', '').replace('us', '').split(':')[1]
            if ind % 3 == 0:
                comp_avg += float(line.split(',')[0])
            if (ind - 1) % 3 == 0:
                mem_avg += float(line.split(',')[0])
        comp_avg /= 3
        mem_avg /= 3
        print(mem_avg, comp_avg)


read_vm_characteristics('util.txt')
# print(get_info("1580912688;wlp2s0;0.00;4141.72;4141.72;2075;0;0.00;59.88;59.88;30;0;0.00;0.00;0;0","bytes_in/s"))
