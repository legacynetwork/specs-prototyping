# specs-prototyping

A minimalist python prototype emulating Legacy's application functionalities and architecture
## Service Description

*Disclaimer: this is a work in progress for engineering purposes only and not meant to be used in practical applications.*

## Requirements

Should work on most Python 2.X versions (tested on 2.7.5). You may install package requirements using `pip`:

`pip install -r requirements.txt`

## Overview

This prototype aims to provide the most basic functionalities to be integrated in the new proof of concept already under development. Essentially, it is a *decentralised dead man switch*. Its main functionalities should be:

- Sending funds from a user smart contract to a given set of `n` recipient addresses (aka as beneficiaries).

- Sending encrypted messages to a given set of recipients. 

### Switch Activation
These actions are to be performed after the user contract shows no sign of activity over a predefined time period `t_PoL`. 

### Assumptions
- Each beneficiary already has an Ethereum account. 

Some additional desired features:

- The amount of funds to be sent to each beneficiary is only revealed once the minimum set of conditions to transfer the funds is met.

### Output
The current python prototype provides as output two secrets that must be given to each beneficiary, that is, a *secret piece* along with a *personal decryption password*:	
```
- address 0x0
    secret piece: 1-46564ca4
    personal decryption password: jIcYWOi8EnUtb_4RLffqrJLG0Ygb5h1RAo3S7RSFb0I=


- address 0x1
    secret piece: 2-b68745f
    personal decryption password: ojTO_xfmqUiY_5AyanVnW15apsaiohbB8erue8FW3J4=


- address 0x2
    secret piece: 3-507a9c19
    personal decryption password: 3bW-vmZ67wVbVEbOdSdfuyc_tYLIZvwXLTr2L0WfvUA=
```


### Encryption/Decryption System

Files should be encrypted and stored in IPFS nodes. Two encryption layers are applied: the first uses a symmetric key which is only known by the corresponding recipient `i`. The second uses a shared key of which all beneficiaries hold a share. If `n` the total amount of beneficiaries, then the shared key can be retrieved if and only if `k` out of `n` key shares are provided. The parameter `k` (`1 <= k <= n`) is defined by the user upon system setup.

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

- With this simple design, it is difficult to add/remove beneficiaries once everything has been set. A new contract must be generated and new secrets must be sent to the new set of beneficiaries.
- Since all beneficiaries are provided by the user at once, the code should be optimized to minimise transactions.




