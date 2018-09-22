from legacy.contracts import LegacyUserContract, Wallet, Ethereum
from user_app import store_file_in_ipfs
from beneficiary_app import read_file_from_ipfs    
from util.cipher import AESCipher
from util.util import load_object, say
from secretsharing import PlaintextToHexSecretSharer
from cryptography.fernet import Fernet
from hashlib import sha256
import os, re
import config

# parameters
contract_name = 'test_contract'
owner = '0xnflu0c8ml2maxpc6h30r3am2qyaeok5labd1po5f'
# these are the accounts of the beneficiaries
addresses = [
    'test_0x41k2qiianhyajppzd5avvrp12wbn42y0m2k70y5c',
    'test_0x9q6v0r516hrk7kvn0ixojefu6diyoblvj5urlo70',
    'test_0xn8b77b6nmo14ozrr00gcy0ccirlpyw2hs31a9k0f'
    ]
message_files = addresses        
n = 3
k = 2
secret_messages =(
    "Luke, I'm your father",
    "Get my ETH. My private key is 3a1076bf45ab87712ad64ccb3b10217737f7faacbf2872e88fdd9a537d8fe266",
    "My computer password is 3KS014Q. Do whatever you see fit with that"
    )
share_of_funds = ('50%', '25%', '25%')
secret = "I've seen things you people wouldn't believe"
t_PoL = 90
init_balance = 100 # user has 100 eth to distribute

# params = {
#     'contract_name': 'test_contract',
#     'owner' = '0xnflu0c8ml2maxpc6h30r3am2qyaeok5labd1po5f',
#     'addresses': [  # these are the accounts of the beneficiaries
#         'test_0x41k2qiianhyajppzd5avvrp12wbn42y0m2k70y5c',
#         'test_0x9q6v0r516hrk7kvn0ixojefu6diyoblvj5urlo70',
#         'test_0xn8b77b6nmo14ozrr00gcy0ccirlpyw2hs31a9k0f'
#     ],
#     'message_files': addresses,
#     'n': 3,
#     'k': 2,
#     'secret_messages': (
#         "Luke, I'm your father",
#         "Get my ETH. My private key is 3a1076bf45ab87712ad64ccb3b10217737f7faacbf2872e88fdd9a537d8fe266",
#         "My computer password is 3KS014Q. Do whatever you see fit with that"
#     ),
#     'share_of_funds': ('50%', '25%', '25%'),
#     'secret': "I've seen things you people wouldn't believe",
#     't_PoL': 90,
#     'init_balance': 100 # user has 100 eth to distribute
# }

# def create_test_scenario(params):    
#     # retrieve parameters
#     contract_name = params['contract_name']
#     owner = params['owner']
#     addresses = params['addresses']    
#     message_files = params['message_files']
#     n = params['n']    
#     k = params['k']    
#     secret_messages = params['secret_messages']
#     share_of_funds = params['share_of_funds']
#     secret = params['secret']
#     t_PoL = params['t_PoL']
#     init_balance = params['init_balance']

#     secret_low = secret.lower()
#     secret_pieces = PlaintextToHexSecretSharer.split_secret(secret_low, k, n)
#     # create encryption object based on shared secret
#     aes_cipher = AESCipher(secret_low)
    
#     beneficiaries = []
#     personal_keys = []
#     enc_messages = []
#     doub_enc_messages = []
#     for i in range(n):
#         wallet_i = Wallet(addresses[i]) # creates a wallet with random address
#         wallet_i.save()
#         personal_keys.append(Fernet.generate_key())
#         cipher_suite = Fernet(personal_keys[i])    
#         enc_messages.append(cipher_suite.encrypt(secret_messages[i]))    
#         doub_enc_messages.append(aes_cipher.encrypt(enc_messages[i]))
#         message_url_i = store_file_in_ipfs(doub_enc_messages[i], message_files[i])      
#         funds_share_i = share_of_funds[i]                 
#         beneficiaries.append({'wallet_address': wallet_i.address, 'message_url': message_url_i, 
#             'funds_share': funds_share_i, 'secret_piece_hash': sha256(secret_pieces[i]).hexdigest()})
        
#     user_contract = LegacyUserContract(k, n, t_PoL, init_balance, beneficiaries, owner, contract_name)
#     user_contract.save(contract_name)
#     contract_state = hash(user_contract)
#     return contract_state, secret_pieces, enc_messages, doub_enc_messages, personal_keys, beneficiaries

def create_test_scenario():    
    secret_low = secret.lower()
    secret_pieces = PlaintextToHexSecretSharer.split_secret(secret_low, k, n)
    # create encryption object based on shared secret
    aes_cipher = AESCipher(secret_low)
    
    beneficiaries = []
    personal_keys = []
    enc_messages = []
    doub_enc_messages = []
    for i in range(n):
        wallet_i = Wallet(addresses[i]) # creates a wallet with random address
        wallet_i.save()
        personal_keys.append(Fernet.generate_key())
        cipher_suite = Fernet(personal_keys[i])    
        enc_messages.append(cipher_suite.encrypt(secret_messages[i]))    
        doub_enc_messages.append(aes_cipher.encrypt(enc_messages[i]))
        message_url_i = store_file_in_ipfs(doub_enc_messages[i], message_files[i])      
        funds_share_i = share_of_funds[i]                 
        beneficiaries.append({'wallet_address': wallet_i.address, 'message_url': message_url_i, 
            'funds_share': funds_share_i, 'secret_piece_hash': sha256(secret_pieces[i]).hexdigest()})
        
    user_contract = LegacyUserContract(k, n, t_PoL, init_balance, beneficiaries, owner, contract_name)
    user_contract.save(contract_name)
    contract_state = hash(user_contract)
    return contract_state, secret_pieces, enc_messages, doub_enc_messages, personal_keys, beneficiaries

def purge_test_scenario():    
    # deletes all files in the data directory whose name start with 'test_'
    for f in os.listdir(config.DATA_DIR):
        file_path = os.path.join(config.DATA_DIR, f)        
        if os.path.isfile(file_path) and f.startswith("test_"):            
            os.remove(file_path)                  


if __name__ == '__main__':

    contract_state, secret_pieces, enc_messages, doub_enc_messages, personal_keys, beneficiaries = create_test_scenario()    

    # test object load
    user_contract = LegacyUserContract.load(contract_name)
    if contract_state != hash(user_contract):
        say("An error occurred while loading the contract object.", 2)    

    # try to recover secret with 1 out of 3 secret shares (should fail)
    try:
        recov_secret = PlaintextToHexSecretSharer.recover_secret(secret_pieces[0])
    except:
        pass
    else:
        say("This is weird. It shouldn't be possible to recover a secret with only one piece", 2)

    # try to recover secret with 2 out of 3 secret shares (should work)
    try:
        recov_secret = PlaintextToHexSecretSharer.recover_secret(secret_pieces[0:2])
    except:
        say("Could not recover secret.", 2)

    # check if recovered secret matches original one
    if recov_secret != secret.lower():
        say('Error. The recovered secret does not match the original one', 2)    

    # save secrets in contract and recover secret
    for i in range(0, n):
        user_contract.save_secret_piece(secret_pieces[i], beneficiaries[i]['wallet_address'])
    user_contract.save(contract_name)

    del user_contract
    user_contract = LegacyUserContract.load(contract_name)

    # after saving, secret should have been recovered
    if recov_secret != user_contract.secret:
        say("Error. Recovered secret mismatch.", 2)

    # testing proof of life related functions
    # since we just created the contract, user should be alive
    if not user_contract.is_active():
        say("Error. User should be alive", 2)
    t0 = user_contract.PoL_limit
    user_contract.proof_of_life()
    if user_contract.PoL_limit - t0 != user_contract.t_PoL:
        say("Error with proof_of_life() method", 2)

    aes_cipher = AESCipher(recov_secret)

    # decrypt messages (from array in memory)
    for i in range(0, n):
        # first decryption step
        enc_message_i_prime = aes_cipher.decrypt(doub_enc_messages[i])
        if enc_message_i_prime != enc_messages[i]:
            say("Error, decrypted message using shared secret doesn't match original", 2)        
            print enc_message_i_prime + '\n' + enc_messages[i] + '\n'

        # second decryption step    
        cipher_suite = Fernet(personal_keys[i])
        message_i_prime = cipher_suite.decrypt(enc_message_i_prime)
        if message_i_prime != secret_messages[i]:
            say("Error, decrypted message using personal key doesn't match the original one", 2)        
            print message_i_prime + '\n' + secret_messages[i] + '\n'


    # decrypt messages (from stored files)
    # tests read_file_from_ipfs(index, filename="")
    for i in range(n):
        doub_enc_message = read_file_from_ipfs(message_files[i])
        
        # first decryption step
        enc_message_i_prime = aes_cipher.decrypt(doub_enc_message)
        if enc_message_i_prime != enc_messages[i]:
            say("Error, decrypted message using shared secret doesn't match original", 2)        
            print enc_message_i_prime + '\n' + enc_messages[i] + '\n'

        # second decryption step    
        cipher_suite = Fernet(personal_keys[i])
        message_i_prime = cipher_suite.decrypt(enc_message_i_prime)
        if message_i_prime != secret_messages[i]:
            say("Error, decrypted message using personal key doesn't match the original one", 2)        
            print message_i_prime + '\n' + secret_messages[i] + '\n'



    say("success!", 1)

    # clean up data directory  
    purge_test_scenario()    
       
    



