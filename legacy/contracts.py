
class LegacyUserContract:
    """An emulated smart contract which implements basic functionalities. For prototyping purposes only"""

    def __str__(self):
        return "Contract " + self.owner
        
    def __init__(self, k=2, n=2, t_PoL=90, init_deposit=0, beneficiaries=[], owner_address='0x'):
        # initialize state variables
        self.k = k
        self.n = n
        self.t_PoL = t_PoL # in days
        self.balance = init_deposit
        self.is_alive = True
        self.beneficiaries = beneficiaries # an array of Beneficiary tuples
        self.owner = owner_address
        #self.address = '0x...'        

    def proof_of_life():
        pass

    def save_secret_piece(k_i, address_i):
        pass

    def set_shared_secret(k):
        pass

    def transfer_funds():
        pass

    def add_recipient(recipient_address, funds_share):
        pass

    def is_active():
        pass
