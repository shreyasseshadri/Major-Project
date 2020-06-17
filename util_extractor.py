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
    comp_count = 0
    comp_avg = 0

    mem_count = 0
    mem_avg = 0

    network_count = 0
    network_avg = 0
    with open(util_file, 'r') as f:
        for ind, line in enumerate(f.readlines()):
            line = line.replace('\n', '').replace('\t', '').replace(' ', '')
            if line.find('id:') >= 0 :
                vm_id = line.split(':')[1]
                continue
            if ind >= 9:
                network_avg += float(get_network_info(line, 'bytes_total/s'))
                network_count += 1
            else:
                line = line.replace('total', '').replace('us', '').replace('free','').replace('%','').replace('k','').split(':')[1]
                if ind % 3 == 0:
                    comp_avg += float(line.split(',')[0])
                    comp_count += 1
                elif (ind - 1) % 3 == 0:
                    try:
                        mem_avg += float(line.split(',')[2])
                    except:
                        mem_avg += float(line.split(',')[1])
                    mem_count += 1
        comp_avg /= comp_count
        mem_avg /= mem_count
        network_avg /= network_count

        return (mem_avg, comp_avg, network_avg,vm_id)

if __name__ == "__main__":
    print(read_vm_characteristics('sample.txt'))
    print(read_vm_characteristics('util0.txt'))
