from .app import app
from .models import db
from flask import render_template, request, flash, redirect, abort
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime
from pony.orm import flush
import base64
import hashlib
from .web3_utils import *


def hash_str(s):
    hasher = hashlib.sha1(s.encode())
    return base64.urlsafe_b64encode(hasher.digest()[:10]).decode()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if "eth-address" in request.form.keys():
            # tip payment
            user = db.User.get(eth_address=request.form['eth-address'])
            if user:
                return redirect(f"pay/{user.hash}")
            else:
                flash('Such wallet is not registered :(', category='error')
                return redirect('/')
        if "amount" in request.form.keys():
            # token sell
            hex = sell_tokens(current_user.eth_address,
                              int(request.form["amount"]), erc20_contract, dex_contract).hex()
            return render_template('index.html', token_balance=token_balance, ether_balance=ether_balance, transaction_hash=hex)
        else:
            # login
            username = request.form['email']
            password = request.form['password']

            possible_user = db.User.get(login=username)
            if not possible_user:
                flash('Such email is not registered :(', category='error')
                return redirect('/')
            if possible_user.password == password:
                possible_user.last_login = datetime.now()
                login_user(possible_user)
                return redirect('/')

            flash('Wrong password', category='error')
            return redirect('/')
    else:
        return render_template('index.html', token_balance=token_balance, ether_balance=ether_balance)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        name = request.form['name']
        surname = request.form['surname']
        eth_address = request.form['eth-address']
        photo_url = request.form['photo-url']

        exist = db.User.get(login=username)
        if exist:
            flash('Username %s is already taken, choose another one' % username)
            return redirect('/reg')

        user = db.User(login=username,
                       password=password,
                       eth_address=eth_address,
                       name=name,
                       surname=surname,
                       photo_url=photo_url)
        user.last_login = datetime.now()
        user.hash = hash_str(user.login + user.name)
        flush()
        login_user(user)
        flash('Successfully registered')
        return redirect('/')
    else:
        return render_template('reg.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect('/')


@app.route('/pay/<user_hash>', methods=['GET', 'POST'])
def pay(user_hash):
    if request.method == 'POST':
        address = request.form['address']
        amount = request.form['amount']

        buy_tokens(address, amount, dex_contract)
        transaction = transfer_tokens(amount, db.User.get(
            hash=user_hash).eth_address, address, erc20_contract)
        return render_template('success.html', transaction_hash=transaction.transactionHash.hex())
    else:
        return render_template('pay.html', user=db.User.get(hash=user_hash))
