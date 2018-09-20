from secretsharing import PlaintextToHexSecretSharer
from datetime import datetime, timedelta
from string import ascii_lowercase, digits
from random import choice
from hashlib import sha256
from util.util import save_object, load_object
import config
import os

# TODO: 
# - current version of the contract assumes that each beneficiary holds
#   a secret piece (len(beneficiaries = n)). The real app should be more flexible
#   and separate secret keepers from beneficiaries
# - LegacyUserContract and Wallet should inherit from EthereumAccount, which has methods
#   save(), load() and get_new_address()

class LegacyUserContract:
    """An emulated smart contract which implements basic functionalities. For prototyping purposes only"""

    def __str__(self):
        return "Contract " + self.address
        
    def __init__(self, k=2, n=3, t_PoL=90, init_deposit=0, beneficiaries=[], owner="", name=""):
        # initialize state variables
        self.k = k
        self.n = n
        self.t_PoL = timedelta(t_PoL) # in days
        self.PoL_limit = datetime.now().date() + self.t_PoL
        self.balance = init_deposit        
        self.beneficiaries = beneficiaries # a list of dictionaries        
        self.collected_secrets = []
        self.secret = ""
        self.address = Ethereum.get_new_address()
        self.contract_name = name if name else 'user_contract' # a human-readable name
        self.owner = owner if owner else Ethereum.get_new_address()

    def __hash__(self):
        return hash((self.owner, self.k, self.n, self.balance, self.t_PoL))

    def proof_of_life(self):
        self.PoL_limit = self.PoL_limit + self.t_PoL

    def save_secret_piece(self, secret_piece, address):
        for i in range(0, self.n):
            if (self.beneficiaries[i]['wallet_address'] == address and
                self.beneficiaries[i]['secret_piece_hash'] == sha256(secret_piece).hexdigest()):
                self.collected_secrets.append(secret_piece)
                if len(self.collected_secrets) >= self.k:
                    self.recover_shared_secret()
                return True
        return False

    def recover_shared_secret(self):
        # TODO: manage exceptions
        if len(self.collected_secrets) >= self.k:
            self.secret = PlaintextToHexSecretSharer.recover_secret(self.collected_secrets)

    def deposit(self, value):
        self.balance = self.balance + value

    def transfer_funds():
        if not self.is_active():
            # transfer funds
            pass

    def add_recipient(recipient_address, funds_share):
        pass

    def is_active(self):
        #return datetime.now().date() <= self.PoL_limit + self.PoL_margin # TODO add margin
        return datetime.now().date() <= self.PoL_limit

    def has_beneficiary(self, address):
        for i in range(0, self.n):
            if self.beneficiaries[i]['wallet_address'] == address:
                return True

    def save(self, filename=""):
        if filename:
            save_object(self, os.path.join(config.DATA_DIR, filename + '.pkl'))
        else:
            save_object(self, os.path.join(config.DATA_DIR, self.contract_name + '.pkl'))

    @staticmethod
    def load(contract_name):
        return load_object(os.path.join(config.DATA_DIR, contract_name + '.pkl'))



class Wallet:
    """ A very simple class emulating an Ethereum Wallet """

    def __init__(self, address=""):
        self.address = address if address else Ethereum.get_new_address()        
        self.balance = 0        

    def save(self, filename=""):
        if filename:
            save_object(self, os.path.join(config.DATA_DIR, filename + '.pkl'))
        else:
            save_object(self, os.path.join(config.DATA_DIR, self.address + '.pkl'))        


class Ethereum:    

    @staticmethod
    def get_new_address():
        # returns a pseudo-random string of length ADDRESS_LEN using only ASCII lowercase letters and digits        
        return '0x' + ''.join(choice(ascii_lowercase + digits) for _ in range(config.ADDRESS_LEN)) 
        

