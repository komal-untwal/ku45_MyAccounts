import logging

from app import db
from app.db.models import User, Accounts
from faker import Faker


def test_adding_user(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Accounts).count() == 0
        # showing how to add a record
        # create a record
        user = User('ku45@test.com', 'testtest')
        # add it to get ready to be committed
        db.session.add(user)
        # call the commit
        # db.session.commit()
        # assert that we now have a new user
        # assert db.session.query(User).count() == 1
        # finding one user record by email
        user = User.query.filter_by(email='ku45@test.com').first()
        log.info(user)
        # asserting that the user retrieved is correct
        assert user.email == 'ku45@test.com'
        # this is how you get a related record ready for insert
        user.accounts = [Accounts(2000, "CREDIT"), Accounts(-1000, "DEBIT")]
        # commit is what saves the accounts
        db.session.commit()
        assert db.session.query(Accounts).count() == 2
        account1 = Accounts.query.filter_by(amount=2000).first()
        assert account1.amount == 2000
        # changing the amount
        account1.amount = 500
        db.session.commit()
        account2 = Accounts.query.filter_by(amount=500).first()
        assert account2.amount == 500
        # checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Accounts).count() == 0
