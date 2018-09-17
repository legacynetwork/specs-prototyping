from secretsharing import PlaintextToHexSecretSharer
from datetime import datetime, date, timedelta

class LegacyUserContract:
    """An emulated smart contract which implements basic functionalities. For prototyping purposes only"""

    def __str__(self):
        return "Contract " + self.owner
        
    def __init__(self, k=2, n=2, t_PoL=90, init_deposit=0, beneficiaries=[], owner_address='0x0'):
        # initialize state variables
        self.k = k
        self.n = n
        self.t_PoL = timedelta(t_PoL) # in days
        self.PoL_limit = datetime.now().date() + self.t_PoL
        self.balance = init_deposit
        self.is_alive = True
        self.beneficiaries = beneficiaries # an array of Beneficiary tuples
        self.owner = owner_address
        self.collected_secrets = []

    def proof_of_life(self):
        self.PoL_limit = self.PoL_limit + self.t_PoL        

    def save_secret_piece(self, secret_piece, address):
        for i in range(0, n):
            if self.beneficiaries[i]['wallet_address'] == address:
                #self.beneficiaries[i]['secret_piece'] = secret_piece
                self.collected_secrets.append(secret_piece)
                if len(self.collected_secrets) >= self.k:
                    self.recover_shared_secret()        

    def recover_shared_secret(self):
        # TODO: manage exceptions
        if len(self.collected_secrets) >= self.k:
            self.secret = PlaintextToHexSecretSharer.recover_secret(collected_secrets)

    def deposit(self, value):
        self.balance = self.balance + value        

    def transfer_funds():
        pass

    def add_recipient(recipient_address, funds_share):
        pass

    def is_active():        
        return datetime.now().date() <= self.PoL_limit + self.PoL_margin
