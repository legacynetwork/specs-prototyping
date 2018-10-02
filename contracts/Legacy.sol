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
    uint constant SHARE_HASH_LEN = 256; // TODO: define
    uint constant SHARE_LEN = 256; // TODO: define

    // state variables
    uint public k;
    uint public n;
    days public tPoL;
    days public tZero;
    // address public owner;
    byte[SHARE_HASH_LEN][] public hashedSecretShares;
    byte[SHARE_LEN][] public secretShares;
    address[] public beneficiaries;

    struct Beneficiary{
        uint fundsShare;
        byte[] messageUrl;
    }

    mapping(address => Beneficiary) public beneficiaryData;


    // function (param types) {internal|external} [pure|constant|view|payable]
    // [returns (return types)] 

    function constructor(uint _k, uint _n, uint _tPoL, byte[SHARE_HASH_LEN][] _hashedSecretShares) public {
        if(_k > 0 && _n > 0 && _k < _n){
            k = _k;
            n = _n;
        }   
        if(_tPoL > 0) tPoL = _tPoL * 1 days;
        hashedSecretShares = _hashedSecretShares; // TODO: check
     }

    function proofOfLife() public onlyOwner {
        reset_timer();
    }

    function isActive() public return(bool) {
        if (now > t_zero) return false;
        else return true;
    }

    function resetTimer() internal {
        // TODO: make sure cannot be called externally by anyone
        // apart from the owner
        tZero = tZero + tPoL;
    }

    function saveSecretShare(bytes[] _share) public {
        for(uint i = 0; i < hashedSecretShares.length){
            if( sha256(_share) == hashedSecretShares[i])
                secretShares.push(_share);
        }
    }

    function claimFunds(address _beneficiary) public {}

    function isBeneficiary(address _beneficiary) public return(bool) {
        for(uint i = 0; i < beneficiaries.length)
            if( _beneficiary == beneficiaries[i]) return true;
        return false;
    }

    function() public payable {
        if(msg.sender == owner) reset_timer();
    }
    
    function kill() public onlyOwner {}


}