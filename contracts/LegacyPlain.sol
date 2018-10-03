 // simplified contract prototype that does not implement encryption

pragma solidity ^0.4.24;


contract Owned {
    
    address owner;
    
    constructor() public { owner = msg.sender; }
    
    modifier onlyOwner {
        require(
            msg.sender == owner,
            "Only owner can call this function."
        );
        _;
    }
}


contract Legacy is Owned{
    
    // state variables    
    uint256 public tPoL;
    uint256 public tZero;       
    address[] public beneficiaries;

    struct Beneficiary{
        uint256 shareOfFunds;
        string messageUrl; // ipfs url, only one message per beneficiary for now
    }

    mapping(address => Beneficiary) public beneficiaryData;
    
    constructor(uint256 _tPoL) public {        
        if(_tPoL > 0) tPoL = _tPoL * 1 days;
        tZero = now + tPoL;        
     }

    function() public payable {
        if(msg.sender == owner) resetPoLTimer();
    }

    function giveProofOfLife() public onlyOwner {
        resetPoLTimer();
    }

    function getProofOfLife() public view returns(bool) {
        if (now > tZero) return false;
        else return true;
    }

    function resetPoLTimer() internal {
        // TODO: make sure cannot be called externally by anyone
        // apart from the owner
        tZero = tZero + tPoL;
    }

    function setPoLTimerLength(uint256 _tPoL) public onlyOwner {
        if(_tPoL > 0) tPoL = _tPoL * 1 days;
        resetPoLTimer();
    }
    
    function claimFunds(address _beneficiary) public {
        require(isBeneficiary(_beneficiary));
        require(!getProofOfLife());
        _beneficiary.transfer(this.balance/beneficiaries.length);
    }
    
    function addBeneficiary(address _beneficiary, string _messageUrl, uint256 _shareOfFunds) public onlyOwner {
        // TODO: check if input data is valid
        beneficiaryData[_beneficiary].messageUrl = _messageUrl;
        beneficiaryData[_beneficiary].shareOfFunds = _shareOfFunds;
        beneficiaries.push(_beneficiary);
        resetPoLTimer();
    }

    function isBeneficiary(address _beneficiary) public view returns(bool) {
        for(uint8 i = 0; i < beneficiaries.length; i++){
            if( _beneficiary == beneficiaries[i]) return true;
        }
        return false;
    }    

    function withdraw(uint amount) public onlyOwner {
        if (this.balance >= amount) {
            msg.sender.transfer(amount);
        }
        resetPoLTimer();
    }
    
    function kill() public onlyOwner { selfdestruct(owner); }
    
}