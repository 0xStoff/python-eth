pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Airdrop {
    IERC20 public airdropToken;
    address public constant eligibleAddress = 0xCf4bce3Aed2Ff56A03bAE79B1C97710A9F9dD0f5;

    constructor(address _airdropTokenAddress) {
        airdropToken = IERC20(_airdropTokenAddress);
    }

    function claim() external {
        require(msg.sender == eligibleAddress, "Caller is not eligible to claim tokens.");
        uint256 airdropAmount = 100 * 10**18; // 100 tokens with 18 decimals
        require(airdropToken.transfer(msg.sender, airdropAmount), "Token transfer failed.");
    }
}
