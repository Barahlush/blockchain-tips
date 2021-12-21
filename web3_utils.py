import json
from web3 import Web3
import os
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))


def connect_contract(contract_address, abi_file):
    with open(abi_file, 'r') as f:
        abi = json.load(f)
    contract = w3.eth.contract(contract_address, abi=abi)
    return contract


erc20_addr = "0xD26B1D179e919D7c8fA47563Adad9558363E1c81"
dex_addr = "0x7B2e4d0ad3111069796A510DB3F1F561076D1D30"

erc20_contract = connect_contract(erc20_addr, "blockchain-tips/static/assets/abi.txt")
dex_contract = connect_contract(dex_addr, "blockchain-tips/static/assets/abi_dex.txt")


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
