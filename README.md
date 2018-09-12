# specs-prototyping
A basic, general description of the application architecture and some prototypes.

## Service Description

This prototype version aims to provide the most basic functionalities to be integrated in the new proof of concept already under development. These include:

- Sending funds from a user smart contract to a given set of recipient addresses (aka as beneficiaries).

- Sending encrypted data to a given set of recipients. 

This system assumes that each beneficiary already has an Ethereum account. 

Some additional features:

- The amount of funds to be sent to each beneficiary is only revealed once the minimum set of conditions to transfer the funds is met.

### Switch Activation
The actions mentioned above are performed after the user contract shows no sign of activity over a predefined time period `t_PoL`.

### Encryption/Decryption System

Files are encrypted and stored in IPFS nodes. Two encryption layers are applied: the first uses a symmetric key which is only known by the corresponding recipient `i`. The second uses a shared key of which all beneficiaries hold a share. If `n` the total amount of beneficiaries, then the shared key can be retrieved if and only if `k` out of `n` key shares are provided. The parameter `k` (`1 <= k <= n`) is defined by the user upon system setup.

## The Legacy Main User Contract

### State Variables
- `beneficiary[n] beneficiaries`, where `beneficiary` is a `struct` with fields:  
    - `address wallet`
    - `byte[] message_url`
    - `uint share`
    - `byte[SECRET_LEN] secret_piece`

- `bytes[SECRET_LEN] secret`

- `uint k`

- `uint n`

- `bool is_alive`

- `days t_PoL`

### Parameters
- `uint SECRET_LEN`


### Contract Interface

- `function proof_of_life() public`
- `function save_secret_piece(uint k_i) public`
- `function set_shared_secret(uint k) public`
- `function transfer_funds() public`
- `function add_recipient(address _recipient, uint _percentage) public`
- `function is_active() public view returns(bool)`

## Current Limitations and Some Observations

- It is currently difficult to add/remove beneficiaries once everything has been set. A new contract must be generated and new secrets must be sent to the new set of beneficiaries.
- Since all beneficiaries are provided by the user at once, the code should be optimized to minimise transactions.




