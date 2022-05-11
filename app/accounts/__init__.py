import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Accounts, User
from app.accounts.forms import csv_upload
from werkzeug.utils import secure_filename, redirect
from sqlalchemy.sql import functions

accounts = Blueprint('accounts', __name__,
                     template_folder='templates')


# @songs.route('/accounts', methods=['GET'], defaults={"page": 1})
# @songs.route('/accounts/<int:page>', methods=['GET'])
# def songs_browse(page):
#     page = page
#     per_page = 1000
#     pagination = Accounts.query.filter_by(user_id=current_user.id).paginate(page, per_page, error_out=False)
#     data = pagination.items
#     try:
#         return render_template('total_balance.html', data=data, pagination=pagination)
#     except TemplateNotFound:
#         abort(404)


@accounts.route('/accounts', methods=['GET'], defaults={"page": 1})
@accounts.route('/accounts/<int:page>', methods=['GET'])
def total_balance(page):
    user_obj = User.query.get(current_user.id)
    accounts_page = page
    accounts_per_page = 1000
    pagination = Accounts.query.filter_by(user_id=current_user.id).paginate(accounts_page, accounts_per_page,
                                                                            error_out=False)
    data = pagination.items
    balance = user_obj.balance

    try:
        return render_template('total_balance.html', data=data, pagination=pagination, balance=balance)
    except TemplateNotFound:
        abort(404)


@accounts.route('/accounts/upload', methods=['POST', 'GET'])
@login_required
def accounts_upload():
    form = csv_upload()

    balance = 0.0
    if form.validate_on_submit():
        log = logging.getLogger("csvUploads")
        log.info('csv upload successful!')

        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        user = current_user
        list_of_accounts = []
        with open(filepath) as file:
            #field_names = ['AMOUNT', 'TYPE']
            csv_file = csv.DictReader(file)
            for row in csv_file:
                # print(row)
                transaction = Accounts(row['\ufeffAMOUNT'], row['TYPE'])
                list_of_accounts.append(transaction)
                db.session.add(transaction)
                balance = balance + float(transaction.amount)

        user.accounts = list_of_accounts
        user.balance = balance
        db.session.commit()

        return redirect(url_for('accounts.total_balance'))

    #user_obj = User.query.get(current_user.id)
    #user_bal = user_obj.balance

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)

# @accounts.route('/accounts', methods=['GET'], defaults={"page": 1})
# @accounts.route('/accounts/<int:page>', methods=['GET'])
# def balance_cal():
#     balance = Accounts.query(functions.sum(Accounts.amount)).group_by(Accounts.user_id)
#     print("balanace ", balance)
#     return balance
