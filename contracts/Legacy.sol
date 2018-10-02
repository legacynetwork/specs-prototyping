pragma solidity ^0.4.24;

contract Owned {
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


contract Legacy is Owned{

    // constant parameters
    uint constant SECRET_LEN = 256; // TODO: define

    // state variables
    uint public k;
    uint public n;
    days public tPoL;
    days public tZero;
    // address public owner;
    byte[256][] public hashedSecretShares;
    address[] public beneficiaries;

    struct Beneficiary{
        uint fundsShare;
        byte[] messageUrl;
    }

    mapping(address => Beneficiary) public beneficiaryData;


    // function (param types) {internal|external} [pure|constant|view|payable]
    // [returns (return types)] 

    function Legacy() public {

     }

    function proofOfLife() public onlyOwner {
        reset_timer();
    }

    function isActive() public return(bool) {
        // if (now > t_zero) return false;
        // else return true;            
    }

    function resetTimer() internal {
        // make sure cannot be called externally by anyone
        // apart from the owner
        // t_zero = t_zero + t_PoL;
    }

    function saveSecretShare(bytes[] _share) public {}

    function claimFunds() public {}

    function() public payable {
        // if(msg.sender == owner) reset_timer();
    }
    
    function kill() public onlyOwner {}


}