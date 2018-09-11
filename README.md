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
The actions mentioned above are performed after the user contract shows no sign of activity over a predefined time period `T_p`.

### Encryption/Decryption System

Files are encrypted and stored in IPFS nodes. Two encryption layers are applied: the first uses a symmetric key which is only known by the corresponding recipient `i`. The second uses a shared key of which all beneficiaries hold a share. If `n` the total amount of beneficiaries, then the shared key can be retrieved if and only if `k` out of `n` key shares are provided.



