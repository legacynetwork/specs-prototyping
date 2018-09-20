import pickle, os
import config

# colors for printing debug messages
COLORS = {
    0: '\033[0m',  # end color
    1: '\033[93m', # warning
    2: '\033[91m'  # fail
}

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    with open(filename, 'rb') as input_buff:
        return pickle.load(input_buff)

def say(msg, level=0):
    print COLORS[level] + msg + COLORS[0]

# TODO: test
def purge(accounts=[]):
    if accounts:
        files = list(os.path.join(config.DATA_DIR, acc + '.pkl') for acc in accounts)
    else:
        files = list(os.path.join(config.DATA_DIR, f) for f in os.listdir(config.DATA_DIR))
    for f in files:    
        # to only search for valid addresses, add condition:
        # re.search('^0x\w*\.pkl\Z', f)
        if os.path.isfile(f):
            os.remove(f)


