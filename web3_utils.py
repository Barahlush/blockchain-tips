import json
from web3 import Web3
import os
from dotenv import dotenv_values
config = dotenv_values("blockchain-tips/.env")

w3 = Web3(Web3.HTTPProvider(config["BLOCKCHAIN_HTTP_ADDRESS"]))


def connect_contract(contract_address, abi_file):
    with open(abi_file, 'r') as f:
        abi = json.load(f)
    contract = w3.eth.contract(contract_address, abi=abi)
    return contract


erc20_addr = config["ERC20_ADDRESS"]
dex_addr = config["DEX_ADDRESS"]

erc20_contract = connect_contract(
    erc20_addr, config["ERC20_ABI_PATH"])
dex_contract = connect_contract(
    dex_addr, config["DEX_ABI_PATH"])


def get_erc20_decimals(contract=erc20_contract):
    dec = contract.functions.decimals().call()
    return 10 ** dec


def buy_tokens(buyer_address: str, amount_wei: int, dex_contract):
    return dex_contract.functions.buy().transact({"from": buyer_address, "value": amount_wei})


def sell_tokens(seller_address: str, amount_tokens: int, erc20_contract, dex_contract):
    erc20_contract.functions.approve(
        dex_contract.address, amount_tokens).transact({"from": seller_address})
    return dex_contract.functions.sell(amount_tokens).transact({"from": seller_address})


def transfer_tokens(amount_tokens, to_address, from_address, erc20_contract=erc20_contract):
    erc20_contract.functions.approve(
        to_address, int(amount_tokens)).transact({'from': from_address})
    tx_hash = erc20_contract.functions.sendTips(
        to_address, int(amount_tokens)).transact({'from': from_address})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt


def ether_balance(addr):
    return w3.fromWei(w3.eth.get_balance(addr), "ether")


def token_balance(addr, erc20_contract=erc20_contract, account_decimals=False):
    balance = erc20_contract.functions.balanceOf(addr).call()
    if account_decimals:
        balance /= get_erc20_decimals(erc20_contract)
    return balance
