pragma solidity ^0.6.0;


interface IERC20{

    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);

    function transfer(address recipient, uint256 amount)  external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);


    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}


contract ERC20Tip is IERC20 {

    string public constant name = "TIPtoken";
    string public constant symbol = "TTN";
    uint8 public constant decimals = 18;

    uint8 public constant tokenPrice = 5;

    address private common = 0xA4c339CC8259a6B271c12799D5284235B4F33a73;
    uint256 public constant common_commision_percent = 1;
    uint256 public constant min_commision = 1;


    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
    event Transfer(address indexed from, address indexed to, uint tokens);


    mapping(address => uint256) balances;

    mapping(address => mapping (address => uint256)) allowed;

    uint256 totalSupply_ = 10 ether;

    using SafeMath for uint256;

    constructor() public {
        balances[msg.sender] = totalSupply_;
    }

    function totalSupply() public override view returns (uint256) {
        return totalSupply_;
    }

    function balanceOf(address tokenOwner) public override view returns (uint256) {
        return balances[tokenOwner];
    }

    function transfer(address receiver, uint256 numTokens) public override returns (bool) {
        require(numTokens <= balances[msg.sender], "Lack of tokens");
        
        balances[msg.sender] = balances[msg.sender].sub(numTokens);
        balances[receiver] = balances[receiver].add(numTokens);
        emit Transfer(msg.sender, receiver, numTokens);
        return true;
    }

    function approve(address delegate, uint256 numTokens) public override returns (bool) {
        allowed[msg.sender][delegate] = numTokens;
        emit Approval(msg.sender, delegate, numTokens);
        return true;
    }

    function allowance(address owner, address delegate) public override view returns (uint) {
        return allowed[owner][delegate];
    }

    function transferFrom(address owner, address buyer, uint256 numTokens) public override returns (bool) {
        require(numTokens <= balances[owner], "Lack of tokens");
        require(numTokens <= allowed[owner][msg.sender], "Lack of allowed tokens");

        balances[owner] = balances[owner].sub(numTokens);
        allowed[owner][msg.sender] = allowed[owner][msg.sender].sub(numTokens);
        balances[buyer] = balances[buyer].add(numTokens);
        emit Transfer(owner, buyer, numTokens);
        return true;
    }

    function sendTips(address waiter, uint256 numTokens) public returns (bool) {
        uint256 a = min_commision;
        uint256 b = numTokens * common_commision_percent / 100;
        uint256 commisionTokens = a >= b ? a : b;
        uint256 tipsTokens = numTokens - commisionTokens;

        return transfer(waiter, tipsTokens) && transfer(common, commisionTokens);
    }
    /*
    function buy(uint256 _amount) external payable returns (bool) {
        require(msg.value == _amount * tokenPrice, 'Need to send exact amount of wei');
        
        /*
         * sends the requested amount of tokens
         * from this contract address
         * to the buyer
         * /
        return transfer(msg.sender, _amount);
    }

    function sell(uint256 _amount) external returns (bool) {
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] -= _amount;
        // increment the token balance of this contract
        balances[address(this)] += _amount;

        /*
         * don't forget to emit the transfer event
         * so that external apps can reflect the transfer 
        * /
        emit Transfer(msg.sender, address(this), _amount);
        
        // e.g. the user is selling 100 tokens, send them 500 wei
        payable(msg.sender).transfer(_amount * tokenPrice);
    }
    */
}

library SafeMath {
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
      assert(b <= a);
      return a - b;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
      uint256 c = a + b;
      assert(c >= a);
      return c;
    }
}

contract DEX {

    event Bought(uint256 amount);
    event Sold(uint256 amount);
    event Received(address, uint);

    
    
    IERC20 public token;
    
    constructor(address tokenAddress) public {
        token = ERC20Tip(tokenAddress);
    }
    
    function buy() payable public {
        uint256 amountTobuy = msg.value;
        uint256 dexBalance = token.balanceOf(address(this));
        require(amountTobuy > 0, "You need to send some ether");
        require(amountTobuy <= dexBalance, "Not enough tokens in the reserve");
        token.transfer(msg.sender, amountTobuy);
        emit Bought(amountTobuy);
    }

    function sell(uint256 amount) public {
        require(amount > 0, "You need to sell at least some tokens");
        uint256 allowance = token.allowance(msg.sender, address(this));
        require(allowance >= amount, "Check the token allowance");
        token.transferFrom(msg.sender, address(this), amount);
        msg.sender.transfer(amount);
        emit Sold(amount);
    }
    
    receive() external payable {
        emit Received(msg.sender, msg.value);
    }
}
