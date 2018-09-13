from legacy.contracts import LegacyUserContract
from secretsharing import SecretSharer, PlaintextToHexSecretSharer
from cryptography.fernet import Fernet
from collections import namedtuple
from hashlib import sha224
from random import choice
from string import ascii_uppercase, digits

# TO-DO: 
# - n must be at least 2.
# - remove secret_piece from Beneficiary struct
# - consider using dict instead of tuple. eg benefs.append({'wallet': wallet, 'url': url...})
# - do not store secret pieces in contract !

Beneficiary = namedtuple('Beneficiary', ['wallet_address', 'message_url', 'funds_share', 'secret_piece'])

def store_file_in_ipfs(message):
    # just return a random hash for now
    return '/ipfs/Qm' + sha224(message).hexdigest()

# DEPRECATED
# def get_personal_key(LEN):
#     # returns a pseudo-random string of length LEN using only ASCII uppercase letters and digits
#     return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(LEN))

def get_personal_key():
    # returns a 44-char string        
    return Fernet.generate_key()

def get_user_address():
    # in practice, provided through metamask
    # returns a pseudo-random string of length LEN using only ASCII uppercase letters and digits
    LEN = 40
    return '0x' + ''.join(choice(ascii_uppercase + digits) for _ in range(LEN))    
    


print "Setting up your Legacy smart contract. Please provide the following information:"
print "(note: Legacy won't store any kind of sensible data)"

beneficiaries_tmp = []
personal_keys = []
finished = False
finished_input = ""
i = 0
while not finished:    
    address_i = raw_input("Ethereum wallet address of beneficiary " + str(i) + ":" )
    message_i = raw_input("What secret message would you like to leave to this person:")
    personal_key_i = get_personal_key()
    personal_keys.append(personal_key_i)
    cipher_suite = Fernet(personal_key_i)
    message_url_i = store_file_in_ipfs(cipher_suite.encrypt(message_i))
    funds_share_i = raw_input("Share of your funds that you'd like to transfer to this beneficiary:" )
    beneficiaries_tmp.append(Beneficiary(address_i, message_url_i, funds_share_i, ''))
    finished_input = raw_input("Have you finished filling this form (yes/no)?")
    while finished_input not in ['yes', 'no']:
        finished_input = raw_input("Not a valid answer. Try again")
    finished = True if finished_input == 'yes' else False    
    i = i + 1

n = i # number of beneficiaries
secret = raw_input("Now, enter a random phrase that will be used to create your secret password (eg. 'I love cats').") 
secret = secret.lower()
print "Your secret will be shared among " + str(n) + " persons. How many of them will be required to restore it?"
k = raw_input("Please enter an integer k such that 2 <= k < " + str(n))
print "(k,n)=" + "(" + str(k) + "," + str(n) + ")" # DEBUG
print secret
secret_pieces = PlaintextToHexSecretSharer.split_secret(secret, int(k), n)

# TODO: remove this block. secrete pieces are not stored by the system !
# save secrete pieces in each beneficiary struct
beneficiaries = []
for i in range (0, n):
    # fetch data stored in temporal struct 
    wallet_address_i = beneficiaries_tmp[i].wallet_address
    message_url_i = beneficiaries_tmp[i].message_url
    funds_share_i = beneficiaries_tmp[i].funds_share
    # get secrete share corresponding to i beneficiary
    secret_piece_i = secret_pieces[i]
    # save the beneficiary struct in final array
    beneficiaries.append(Beneficiary(wallet_address_i, message_url_i, funds_share_i, secret_piece_i))

print "You will need to give signs of life periodically." 
print "If you fail to so for a time greater than T, we'll assume you are dead."
t_PoL = raw_input("Please enter a value for T (in days):")

user_address = get_user_address()
user_contract = LegacyUserContract(k, n, t_PoL, 0, beneficiaries, user_address)

print "#####################################################################"
print "#################### contract successfully created ! ################"
print "#####################################################################"
print "\n"
print "IMPORTANT: To each one of your beneficiaries, you must give a *secret piece* along with a *personal decryption password*"
print "Once you are dead, your dead man switch can only be activated if "+str(k)+ " out of "+str(n)+" secret pieces are recovered."
print "After that, your beneficiaries will need their *personal decryption password* to decrypt the messages you sent them."
print "Backup this information carefully, and make sure to close this application."
print "\n"
for i in range (0, n):
    print "- address " + beneficiaries[i].wallet_address
    print "    secret piece: " + secret_pieces[i]
    print "    personal decryption password: " + personal_keys[i]
    print "\n" 

print "#####################################################################"
print "######################### program completed #########################"
print "#####################################################################"



