from sys import argv

def open_files():
    try:
        lookup_fp = open(argv[1], 'r')
    except OSError:
        print("could not open file: ", argv[1], ", exiting program")
        exit(-1)
        
    try:
        log_fp = open(argv[2], 'r')
    except OSError:
        print("could not open file: ", argv[2], ", exiting program")
        exit(-1)

    return lookup_fp, log_fp

def close_files(lookup_fp, log_fp):
    lookup_fp.close()
    log_fp.close()

def get_protocol_map():
    protocol_map = {}
    try:
        with open('protocolNums.txt', 'r') as fp:
            for line in fp.read().split('\n'):
                line = line.split()
                if len(line) == 2:
                    protocol_map[line[0]] = line[1]
        return protocol_map
    except OSError:
        print("No file named protocolNums.txt found, please download from https://github.com/pluto-0/IlumioAssessment/tree/master")
        exit(-1)

# First line of lookup csv is redundant
def get_lookup_map(lookup_fp):
    lookup_map = {}
    for line in lookup_fp.read().split('\n')[1:]:
        line = line.split(',')
        lookup_map[(line[0], line[1])] = line[2]
    return lookup_map

# Assumes destination port and protocol nums are always in list spots 6 and 7, respectively
def parse_logs(log_fp, protocol_num_map):
    port_protocol_combos = {}
    for line in log_fp.read().split('\n'):
        if not line:
            continue
        line = line.split(' ')
        try:
            port = line[6]
            protocol = protocol_num_map[line[7]].lower()
        except KeyError:
            print("Unknown protocol number ", line[7], 'exiting program')
            exit(-1)
        if (port, protocol) in port_protocol_combos:
            port_protocol_combos[(port, protocol)] += 1
        else:
            port_protocol_combos[(port, protocol)] = 1
    return port_protocol_combos

def get_tags(port_protocol_combos, protocol_lookup_map):
    tags = {'Untagged': 0}
    for combo in port_protocol_combos:
        if combo in protocol_lookup_map:
            if protocol_lookup_map[combo] in tags:
                tags[protocol_lookup_map[combo]] += 1
            else:
                tags[protocol_lookup_map[combo]] = 1
        else:
            tags['Untagged'] += 1
    return tags

def write_tags(tags, fp):
    fp.write('Tag Counts:\n\n')
    fp.write('Tag, Count\n\n')
    for tag in tags:
        fp.write(tag + ', ' + str(tags[tag]) + '\n\n')

def write_combos(port_protocol_combos, fp):
    fp.write('Port/Protocol Combination Counts:\n\n')
    fp.write('Port, Protocol, Count\n\n')
    for combo in port_protocol_combos:
        fp.write(combo[0] + ', ' + combo[1] + ', ' + str(port_protocol_combos[combo]) + '\n\n')

def write_output(port_protocol_combos, tags):
    with open('output.csv', 'w') as fp:
        write_tags(tags, fp)
        write_combos(port_protocol_combos, fp)

def main():
    '''
    usage: main.py [lookup_file] [log_file]
    '''
    if len(argv) != 3:
        print('usage: main.py [lookup_file] [log_file]')
        exit(-1)
    lookup_fp, log_fp = open_files()
    protocol_num_map = get_protocol_map()
    protocol_lookup_map = get_lookup_map(lookup_fp)
    port_protocol_combos = parse_logs(log_fp, protocol_num_map)
    tags = get_tags(port_protocol_combos, protocol_lookup_map)
    write_output(port_protocol_combos, tags)
    close_files(lookup_fp, log_fp)

if __name__ == '__main__':
    main()