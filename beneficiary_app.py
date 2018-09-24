from util.util import load_object, save_object, say
from util.cipher import AESCipher
from cryptography.fernet import Fernet
from legacy.contracts import Wallet, LegacyUserContract
import os, re, sys
import config


def save_secret_piece():
    # this.secret_piece = secret_piece
    # put secret on the blockchain
    pass

def get_personal_message():
    pass

def get_personal_key():
    pass

def claim_funds():
    pass

def load_or_create_wallet(address):
    try:
        return load_object(os.path.join(config.DATA_DIR, address + '.pkl'))
    except:
        return Wallet()

def read_file_from_ipfs(index, filename=""):
    if not filename:
        filename = index
    file_path = os.path.join(config.DATA_DIR, filename + '.txt')    
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
        return lines[0] # assuming only one line per file
    return None

def load_test_scenario():
    from test import create_test_scenario, contract_name
    create_test_scenario()
    return contract_name

if __name__ == '__main__':

    # if '--test' in sys.argv:
    #   load_test_scenario()
    #   contract_name = 'test_contract'
    # else:
    #   contract_name = 'user_contract'

    contract_name = 'user_contract'

    try:
        user_contract = LegacyUserContract.load(contract_name)
    except:
        say("Error. User Contract not found. Exiting...", 2)
        sys.exit(0)

    print "#####################################################################"
    print "##################### View: beneficiary #############################"
    print "#####################################################################"
    print "\n"

    reg_accounts = []   
    for f in os.listdir(config.DATA_DIR):
        if re.search('^0x\w*\.pkl\Z', f):
            reg_accounts.append(re.split('\.',f)[0])
    if reg_accounts:
        print "The following addresses have been registered in the system:"
        for address in reg_accounts:
            print '\t' + address                        
    benef_address = str(raw_input("Please enter your Ethereum account address:\n"))
    while benef_address not in reg_accounts:
        benef_address = str(raw_input("Not a valid account address. Try again\n"))

    benef = user_contract.get_beneficiary(benef_address)
    if benef:
        print "You are one of the beneficiaries of user " + user_contract.owner + ". You might either:"     
        print "\t1: Provide secrete share"
        print "\t2: Claim funds"
        print "\t3: Recover personal messages"
        option = int(raw_input("Enter an option (1, 2 or 3)\n"))
        while option not in [1, 2, 3]:
            option = int(raw_input("Invalid option, try again\n"))

        if option == 1:
            secret_share = str(raw_input("Please enter your secret share\n"))
            if user_contract.save_secret_piece(secret_share, benef_address):
                user_contract.save()
                say("Your secret share has been successfully saved in the contract.")
            else:
                say("This is not a valid piece. Exiting")
                sys.exit(0)

        elif option == 2:
            pass

        elif option == 3:
            if user_contract.secret:                
                doub_enc_message = read_file_from_ipfs(benef['message_url'])
                if doub_enc_message:
                    aes_cipher = AESCipher(user_contract.secret)
                    key = str(raw_input("Please enter your personal decryption password:\n"))
                    enc_message = aes_cipher.decrypt(doub_enc_message)
                    cipher_suite = Fernet(key)
                    message = cipher_suite.decrypt(enc_message)
                    print "User " + user_contract.owner + " left this message for you:\n"
                    print message
                else:
                    print "Sorry, we didn't find any message for you."




    



