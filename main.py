from sys import argv
from pprint import pprint

def open_files():
    try:
        lookup_fp = open(argv[1], 'r')
    except OSError:
        print("could not open file: ", argv[0], ", exiting program")
        exit(-1)
        
    try:
        log_fp = open(argv[2], 'r')
    except OSError:
        print("could not open file: ", argv[1], ", exiting program")
        exit(-1)

    return lookup_fp, log_fp

def close_files(lookup_fp, log_fp):
    lookup_fp.close()
    log_fp.close()

def get_protocol_map():
    protocol_map = {}
    with open('protocolNums.csv', 'r') as fp:
        for line in fp.read().split('\n'):
            line = line.split()
            if len(line) == 2:
                protocol_map[line[0]] = line[1]
    return protocol_map

# First line of lookup csv is redundant
def get_lookup_map(lookup_fp):
    lookup_map = {}
    for line in lookup_fp.read().split('\n')[1:]:
        line = line.split(',')
        lookup_map[(line[0], line[1])] = line[2]
    return lookup_map

def main():
    '''
    usage: main.py [lookup_file] [log_file]
    '''
    if len(argv) != 3:
        print('usage: main.py [lookup_file] [log_file]')
        exit(-1)
    lookup_fp, log_fp = open_files()
    protocol__map = get_protocol_map()
    lookup_map = get_lookup_map(lookup_fp)
    pprint(lookup_map)
    close_files(lookup_fp, log_fp)

if __name__ == '__main__':
    main()