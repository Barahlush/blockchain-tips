# Blockchain tips
`version 1.1`
Blockchain tips service is a simple example of how one can use ERC20 and DEX smart contracts in order to obtain a decentralized blockchain solution for tips payment and ledgering. This repository contains Flask-based backend and some frontend interfaces as well as original Solidity code for smart contracts. 

**The current version is designed for demonstration and should be run locally with Ganache blockchain.**

## Overview
The server implements a ERC20 token, DEX exchanger and a payment system, described in a picture:

![](https://i.ibb.co/x8yCbCN/image.png)

The service allows to register a profile for some **personal role** (to receive tips). After the registration the person is provided with a personal page and unique QR code which leads to a tip-payment page. Profile contains some personal info (name, surname, blockchain address, photo) as well as account balances. Personal can sell their tokens to the DEX contract in order to get ethereum. 

For a **person who wants to pay tips** the service provide an option to enter Blockchain address, or read QR code (currently not possible). After finding a profile page of a selected staff person, the payer is able to choose amount of ethers to be translated into tokens and payed.

From all the paid tokens, 1% is going to a special address (`common` in `TIPtoken.sol`) (e.g. restaurant wallet), this provides an opportunity for a company to benefit from our service integration.

## Language, Framework and Plugins used :
- Python 3.6.2
- Flask and some extensions (see `requirements.txt`)
- Web3.py
- Pony ORM
- Solidity

## How to use?
1. Download or clone this template.
2. Start [Ganache node](https://github.com/trufflesuite/ganache#getting-started)
3. Connect to the blockchain using [Remix IDE](remix.ethereum.org/)
4. Deploy and setup smart-contracts
   * Set `address private common = 0xA4c339CC8259a6B271c12799D5284235B4F33a73;` in `TIPtoken.sol` to the restorant address to send there 1% of tips
   * Upload `TIPtoken.sol`
   * Deploy ERC20Tip contract
   * Deploy DEX contract, stating the addres of ERC20Tip contract
   * Transact some ethereum to the DEX contract
   * Send all the tokens to the DEX contract
5. [Optional] If you changed the contracts logics, put ABI from contract compilation to files `static/assets/abi.txt` for ERC20Tip contract and `static/assets/abi_dex.txt` for DEX contract (file pathes could be changed in `.env`)
6. Set your contract addresses in `.env`
7. Run `python3 -m blockchain-tips` from parent directory
8. Visit website via url provided by terminal 


## Acknowledgements
**Skoltech "Intro to Blockchain" 2021 course team**
- Yuriy Yanovich
- Yash Madhwal

**Project team**
- Valentin Samokhin
- Pavel Burnishev
- Georgiy Kozhevnikov
