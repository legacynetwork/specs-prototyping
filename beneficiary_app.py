from util.util import load_object, save_object, say
from legacy.contracts import Wallet
import os, re, sys
import config

class Beneficiary:

	def __init__(self):
		# this.address = address
		pass

	def save_secret_piece():
		# this.secret_piece = secret_piece
		# put secret on the blockchain
		pass

	def get_personal_message():
		pass

	@staticmethod
	def get_personal_key():
		pass

	def claim_funds():
		pass

	@staticmethod
	def load_or_create_wallet(address):
		try:
			return load_object(os.path.join(config.DATA_DIR, address + '.pkl'))
		except:
			return Wallet()
			

if __name__ == '__main__':
	
	try:
		user_contract = load_object(os.path.join(config.DATA_DIR, 'user_contract.pkl'))
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

	if user_contract.has_beneficiary(benef_address):
		print "You are one of the beneficiaries of user " + user_contract.owner + ". You might either:"		
		print "\t1: Provide secrete share"
		print "\t2: Claim funds"
		print "\t3: Recover personal messages"
		option = int(raw_input("Enter an option (1, 2 or 3)\n"))
		while option not in [1, 2, 3]:
			option = int(raw_input("Invalid option, try again\n"))

		if option == 1:
			secret_share = str(raw_input("Please enter your secret share\n"))

	

	



