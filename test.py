from legacy.contracts import LegacyUserContract
from util.cipher import AESCipher
from util.util import save_object, load_object, say
from secretsharing import SecretSharer, PlaintextToHexSecretSharer
from cryptography.fernet import Fernet
from random import choice
from string import ascii_uppercase, digits
from hashlib import sha256

n = 3
k = 2

secret_messages =(
    "Luke, I'm your father",
    "Get my ETH. My private key is 3a1076bf45ab87712ad64ccb3b10217737f7faacbf2872e88fdd9a537d8fe266",
    "My computer password is 3KS014Q. Do whatever you see fit with that"
    )

share_of_funds = ('50%', '25%', '25%')

secret = "I've seen things you people wouldn't believe"
secret = secret.lower()
secret_pieces = PlaintextToHexSecretSharer.split_secret(secret, k, n)
# create encryption object based on shared secret
aes_cipher = AESCipher(secret)

t_PoL = 90

beneficiaries = []
personal_keys = []
enc_messages = []
doub_enc_messages = []
for i in range(0, n):
    address_i = '0x' + ''.join(choice(ascii_uppercase + digits) for _ in range(40))         
    personal_keys.append(Fernet.generate_key())
    cipher_suite = Fernet(personal_keys[i])    
    enc_messages.append(cipher_suite.encrypt(secret_messages[i]))    
    doub_enc_messages.append(aes_cipher.encrypt(enc_messages[i]))
    message_url_i =  '/ipfs/Qm' + sha256(doub_enc_messages[i]).hexdigest() # store_file_in_ipfs(doub_enc_message_i)
    funds_share_i = share_of_funds[i]                 
    beneficiaries.append({'wallet_address': address_i, 'message_url': message_url_i, 'funds_share': funds_share_i})
    
user_address = '0x' + ''.join(choice(ascii_uppercase + digits) for _ in range(40))
user_contract = LegacyUserContract(k, n, t_PoL, 0, beneficiaries, user_address)
save_object(user_contract, 'data/user_contract.pkl')

del user_contract

# test object load
user_contract = load_object('data/user_contract.pkl')
print user_contract

# save secrets in contract and recover secret
# for i in range(0, n):
#     user_contract.save_secret_piece(secret_pieces[i])

secret_prime = PlaintextToHexSecretSharer.recover_secret(secret_pieces[0:2])
aes_cipher = AESCipher(secret_prime)

# decrypt messages and transfer funds
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
        say("Error, decrypted message using personal key doesn't match original", 2)        
        print message_i_prime + '\n' + secret_messages[i] + '\n'

    



