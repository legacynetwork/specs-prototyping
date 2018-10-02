pragma solidity ^0.4.24;

contract owned {
    function owned() public { owner = msg.sender; }
    address owner;

    modifier onlyOwner {
        require(
            msg.sender == owner,
            "Only owner can call this function."
        );
        _;
    }
}


contract Legacy is owned{

    // constant parameters
    uint constant SECRET_LEN = 256; // TODO: define

    // state variables
    uint public k;
    uint public n;
    days public t_PoL;
    address public owner;
    address[] public beneficiaries;

    struct Beneficiary{
        uint funds_share;
        byte[] message_url;
    }

    mapping(address => Beneficiary) public beneficiaryData;

    byte[256][] public hashed_secret_shares;

    // function (param types) {internal|external} [pure|constant|view|payable] [returns (return types)] 

    function Legacy() public {}

    function proof_of_life() public {}

    function is_active() public {}    

    function reset_timer() internal{
        // make sure cannot be called externally by anyone
        // apart from the owner
        // t_zero = t_zero + t_PoL;
    }

    function save_secrete_share() public {}

    function claim_funds() public {}

    function() public payable {
        // if(msg.sender == owner) reset_timer();
    }
    
    function kill() public {}


}