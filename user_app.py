from legacy.contracts import LegacyUserContract, Wallet, Ethereum
from util.cipher import AESCipher
from util.util import purge
from secretsharing import SecretSharer, PlaintextToHexSecretSharer
from cryptography.fernet import Fernet
from random import choice
from string import ascii_uppercase, digits
from hashlib import sha256
import sys

# TO-DO: 
# - n must be at least 2.
# - test decrypt
# - test everything actually
# - deprecate fernet and use AES instead
# - store hashes of secrets in the contract

ETH_ACCOUNTS = (
    '0xjjqcouv812rdguinvu9izlsgnhg0t6rahwnzw3ae',
    '0x87akw04kssvmlvvqssl8gvpnghzbmz99oatx0m0h',
    '0xy7ei3dyk3y9ruprxavhbde5qajzm34zpcviufyen',
    '0xc0kgh2crlk1wdfkn4ldha0d4lel0kmv4ue86wegu',
    '0x1rfle3wewrd1psmb0obl8s3as8p296ap5w7phgac'
    )

# in practice, obtained through metamask
USER_ADDRESS = '0xfsefjzd1vpmxokklf6l5n091jatlam4286onamfs'

class LegacyUserApp:

    def __init__():
        pass

    @staticmethod
    def populate_system():
        for i in range(0, len(ETH_ACCOUNTS)):
            account_i = Wallet(ETH_ACCOUNTS[i])
            account_i.save()

    # DEPRECATED
    @staticmethod
    def get_user_address():
        return Ethereum.get_new_address()


def store_file_in_ipfs(message):
    # just return a random hash for now
    return '/ipfs/Qm' + sha256(message).hexdigest()

def get_personal_key():
    # returns a 44-char string        
    return Fernet.generate_key()


if __name__ == '__main__':

    if '--fresh' in sys.argv:
        purge()  # deletes all state data previously stored

    LegacyUserApp.populate_system() # creates some wallets to use as beneficiaries

    print "#####################################################################"
    print "####################### View: User  #################################"
    print "#####################################################################"
    print "\n"        

    print "Set up your Legacy smart contract. Please provide the following information:"
    print "(note: Legacy won't store any kind of sensible data)\n"
    print "### Step 1: Your Beneficiaries"
    print "Existing Ethereum accounts:"
    for i in range(0, len(ETH_ACCOUNTS)):
        print "\t" + ETH_ACCOUNTS[i]

    beneficiaries_tmp = []
    personal_keys = []
    finished = False
    finished_input = ""
    i = 0
    while not finished:    
        address_i = str(raw_input("Ethereum wallet address of beneficiary " + str(i) + ":\n" ))
        # TODO: if address doesn't exist, create it ?
        message_i = raw_input("What secret message would you like to leave to this person:\n")
        personal_key_i = get_personal_key()
        personal_keys.append(personal_key_i)
        cipher_suite = Fernet(personal_key_i)
        enc_message_i = cipher_suite.encrypt(message_i)
        funds_share_i = raw_input("Share of your funds that you'd like to transfer to this beneficiary (eg. 25%):\n" )        
        beneficiaries_tmp.append({'wallet_address': address_i, 'enc_message': enc_message_i, 'funds_share': funds_share_i})
        finished_input = raw_input("Have you finished adding beneficiaries (yes/no)?\n")
        while finished_input not in ['yes', 'no']:
            finished_input = raw_input("Not a valid answer. Try again\n")
        finished = True if finished_input == 'yes' else False    
        i = i + 1

    print "\n### Step 2: The Shared Key"
    n = i # number of beneficiaries
    secret = raw_input("Now, enter a random phrase that will be used to create your secret password (eg. 'I love cats').\n") 
    secret = secret.lower()
    print "Your secret will be shared among " + str(n) + " persons. How many of them will be required to restore it?\n"
    k = int(raw_input("Please enter an integer k such that 2 <= k < " + str(n) + "\n"))
    secret_pieces = PlaintextToHexSecretSharer.split_secret(secret, k, n)
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
        beneficiaries.append({'wallet_address': address_i, 'message_url': message_url_i,
            'funds_share': funds_share_i, 'secret_piece_hash': sha256(secret_pieces[i]).hexdigest()})

    print "\n### Step 3: Proof of Life"
    print "You will need to give signs of life periodically." 
    print "If you fail to so for a time greater than T, we'll assume you are dead."
    t_PoL = int(raw_input("Please enter a value for T (in days):\n"))
            
    user_contract = LegacyUserContract(k, n, t_PoL, 0, beneficiaries, USER_ADDRESS) 
    user_contract.save() # saving with default name 'user_contract'    

    print "#####################################################################"
    print "#################### contract successfully created ! ################"
    print "#####################################################################"
    print "\n"
    print "IMPORTANT: To each one of your beneficiaries, you must give a *secret piece* along with a *personal decryption password*"
    print "If you pass away, your dead man switch can only be activated if "+str(k)+" out of "+str(n)+" secret pieces are recovered."
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



