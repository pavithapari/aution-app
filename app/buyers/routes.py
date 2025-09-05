"""WE can have routes for buyers related routes like their dashboards"""
from flask import Blueprint,render_template,session,redirect,url_for,flash
from app.models import Buyers,Auction,Bid
from app import db
from app.buyers.forms import BuyerReg_form

buyers=Blueprint('buyers',__name__)

def login_required(f):
    from functools import wraps
    from flask import flash
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'user_id' not in session or session.get('role')!='buyer':
            flash("Please login as buyer","warnings")
            return redirect(url_for('auth.login'))
        return f(*args,**kwargs)
    return decorated_function
@buyers.route('/buyer/dashboard')
@login_required
def dashboard():
    return render_template("buyer_dashboard.html")

@buyers.route('/buyer/won')
@login_required
def won_items():
    user_id=session['user_id']
    won_auction=Auction.query.filter_by(winner_id=user_id).all()
    return render_template("buyer_won.html",auctions=won_auctions)


@buyers.route('/buyer/bids')
@login_required
def my_bids():
    user_id = session['user_id']
    bids = Bid.query.filter_by(bidder_id=user_id).all()
    return render_template("buyer_bids.html", bids=bids)


@buyers.route('/buyers/register')
def register():
    form=BuyerReg_form()
    if form.validate_on_submit():
        buyer=Buyers(username=form.name.data,email=form.email.data)
        db.session.add(buyer)
        db.session.commit()

    return render_template('buyer_register.html',buyer_form=form)


@buyers.route('/buyers/show')
def show_buyers():
    buyers=Buyers.query.all()
    return render_template('show.html',buyers=buyers)





