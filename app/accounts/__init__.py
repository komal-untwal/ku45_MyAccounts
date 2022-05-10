import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Accounts
from app.accounts.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

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
    accounts_page = page
    accounts_per_page = 1000
    pagination = Accounts.query.filter_by(user_id=current_user.id).paginate(accounts_page, accounts_per_page,
                                                                            error_out=False)
    data = pagination.items
    try:
        return render_template('total_balance.html', data=data, pagination=pagination)
    except TemplateNotFound:
        abort(404)


@accounts.route('/accounts/upload', methods=['POST', 'GET'])
@login_required
def accounts_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("csvUploads")
        log.info('csv upload successful!')

        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        # user = current_user
        list_of_accounts = []
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                #print(row)
                list_of_accounts.append(Accounts(row['\ufeffAMOUNT'], row['TYPE']))

        current_user.accounts = list_of_accounts
        db.session.commit()

        return redirect(url_for('accounts.total_balance'))

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)
