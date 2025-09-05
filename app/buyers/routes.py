"""WE can have routes for buyers related routes like their dashboards"""
from flask import Blueprint,render_template,flash
from app.models import Buyers
from app import db
from app.buyers.forms import BuyerReg_form
buyers=Blueprint('buyers',__name__)


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



