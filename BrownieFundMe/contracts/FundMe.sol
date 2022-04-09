//SPDX-License_Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;

    }

    // function to fund a contract address given a min amount
    // also maps addresses to amount that they funded 
    function fund() public payable {

        //min amount
        uint256 minUSD = 50 * 10**18; 

        // requires conversion rate of amount to be >= minUSD 
        require(getConversionRate(msg.value) >= minUSD, "You need more ETH!"); 

        // map address to amount using mapping variable declared above
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);

    }

    function getVersion() public view returns (uint256){
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (,int256 answer,,,) = priceFeed.latestRoundData();
         return uint256(answer * 10000000000);
    }


    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount)/1000000000000000000;
        return ethAmountInUsd;
    }

    // modifier changes the behaviour of a function
    modifier onlyOwner {
        // _; // run everything under line below

        // only want contract owner to withdraw funds
        require(msg.sender == owner, "FOH you wanna steal my funds???");
        _; // run everything after line above
    }

    // withdraw all funds and reset all address fundiong balances to 0
    function withdraw() payable onlyOwner public {
        msg.sender.transfer(address(this).balance); // transfer is used to send eth
        for (uint256 i = 0; i < funders.length; i++){
            address funder = funders[i];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }

}