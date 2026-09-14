// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @notice Local educational token. No owner, external mint, tax, or upgrade mechanism.
contract CedarCoin is ERC20 {
    constructor(address recipient) ERC20("Cedar Learning Coin", "CEDAR") {
        _mint(recipient, 1_000_000 * 10 ** decimals());
    }
}
