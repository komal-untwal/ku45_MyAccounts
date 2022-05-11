from app import db
from app.db.models import User, Accounts


def test_user_balance(application):
    # log = logging.getLogger("userBalance")
    balance = 0.0
    with application.app_context():
        # create a record
        user = User('keith@webizly.com', 'testtest')
        db.session.add(user)
        user = User.query.filter_by(email='keith@webizly.com').first()
        # asserting that the user retrieved is correct
        assert user.email == 'keith@webizly.com'
        # check balance before update
        assert user.balance == 0

        user.accounts = [Accounts(5000, "CREDIT"), Accounts(1000, "DEBIT")]
        db.session.commit()

        #check balance for credit transaction
        user_account1 = Accounts.query.filter_by(amount=5000).first()

        if user_account1.trans_type == "CREDIT":
            balance = balance + user_account1.amount
        else:
            balance = balance - user_account1.amount

        user_account1.balance = balance

        assert user_account1.balance == 5000

        # check balance for credit transaction
        user_account2 = Accounts.query.filter_by(amount=1000).first()
        if user_account2.trans_type == "CREDIT":
            balance = balance + user_account2.amount
        else:
            balance = balance - user_account2.amount

        user_account2.balance = balance

        assert user_account2.balance == 4000


