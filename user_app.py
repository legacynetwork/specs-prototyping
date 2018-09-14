from legacy.contracts import LegacyUserContract
from util.cipher import AESCipher
from secretsharing import SecretSharer, PlaintextToHexSecretSharer
from cryptography.fernet import Fernet
from random import choice
from string import ascii_uppercase, digits

# TO-DO: 
# - n must be at least 2.
# - test decrypt
# - test everything actually
# - deprecate fernet and use AES instead

def store_file_in_ipfs(message):
    # just return a random hash for now
    return '/ipfs/Qm' + sha256(message).hexdigest()

def get_personal_key():
    # returns a 44-char string        
    return Fernet.generate_key()

def get_user_address():
    # in practice, provided through metamask
    # returns a pseudo-random string of length LEN using only ASCII uppercase letters and digits
    LEN = 40
    return '0x' + ''.join(choice(ascii_uppercase + digits) for _ in range(LEN)) 
    
print "Setting up your Legacy smart contract. Please provide the following information:"
print "(note: Legacy won't store any kind of sensible data)\n"
print "Step 1: Your Beneficiaries"

beneficiaries_tmp = []
personal_keys = []
finished = False
finished_input = ""
i = 0
while not finished:    
    address_i = raw_input("Ethereum wallet address of beneficiary " + str(i) + ":\n" )
    message_i = raw_input("What secret message would you like to leave to this person:\n")
    personal_key_i = get_personal_key()
    personal_keys.append(personal_key_i)
    cipher_suite = Fernet(personal_key_i)
    enc_message_i = cipher_suite.encrypt(message_i)
    funds_share_i = raw_input("Share of your funds that you'd like to transfer to this beneficiary:\n" )
    #beneficiaries_tmp.append(Beneficiary(address_i, message_url_i, funds_share_i, ''))
    beneficiaries_tmp.append({'wallet_address': address_i, 'enc_message': enc_message_i, 'funds_share': funds_share_i})
    finished_input = raw_input("Any more beneficiaries to include (yes/no)?\n")
    while finished_input not in ['yes', 'no']:
        finished_input = raw_input("Not a valid answer. Try again\n")
    finished = True if finished_input == 'yes' else False    
    i = i + 1

print "\nStep 2: The Shared Key"
n = i # number of beneficiaries
secret = raw_input("Now, enter a random phrase that will be used to create your secret password (eg. 'I love cats').\n") 
secret = secret.lower()
print "Your secret will be shared among " + str(n) + " persons. How many of them will be required to restore it?\n"
k = raw_input("Please enter an integer k such that 2 <= k < " + str(n) + "\n")
secret_pieces = PlaintextToHexSecretSharer.split_secret(secret, int(k), n)
# create encryption object based on shared secret
aes_cipher = AESCipher(secret)

beneficiaries = []
for i in range (0, n):    
    # now that we have the shared secret, apply an additional encryption layer
    doub_enc_message_i = aes_cipher.encrypt(beneficiaries_tmp[i]['enc_message'])    
    message_url_i = store_file_in_ipfs(doub_enc_message_i)
    address_i = beneficiaries_tmp[i]['wallet_address']    
    funds_share_i = beneficiaries_tmp[i]['funds_share']    
    
    # save the beneficiary dict in array (note that we don't store sensible data)
    beneficiaries.append({'wallet_address': address_i, 'message_url': message_url_i, 'funds_share': funds_share_i})

print "\nStep 3: Proof of Life"
print "You will need to give signs of life periodically." 
print "If you fail to so for a time greater than T, we'll assume you are dead."
t_PoL = raw_input("Please enter a value for T (in days):\n")

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
    print "- address " + beneficiaries[i]['wallet_address']
    print "    secret piece: " + secret_pieces[i]
    print "    personal decryption password: " + personal_keys[i]
    print "\n" 

print "#####################################################################"
print "######################### program completed #########################"
print "#####################################################################"



