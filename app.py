from legacy.Contract import LegacyUserContract
from secretsharing import SecretSharer, PlaintextToHexSecretSharer

print "Setting up your Legacy smart contract. Please provide the following information:"
print "(note: Legacy won't store any kind of sensible data)"

finished = False
finished_input = ""
i = 1
while not finished:

    address_i = raw_input("Ethereum wallet address of beneficiary " + str(i) + ":" )
    funds_share_i = raw_input("Share of your funds that you'd like to transfer to this beneficiary " + str(i) + ":" )        
    finished_input = raw_input("Have you finished filling this form (yes/no)?")
    while finished_input not in ['yes', 'no']:
        finished_input = raw_input("Not a valid answer. Try again")
    finished = True if finished_input == 'yes' else False
    i = i + 1


user_contract = LegacyUserContract()

