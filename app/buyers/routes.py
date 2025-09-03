"""WE can have routes for buyers related routes like their dashboards"""
from flask import Blueprint,render_template,flash
from app.models import Buyers
from app import db
buyers=Blueprint('buyers',__name__)


@buyers.route('/buyers/dashboard')
def register():
    buyer=Buyers(username="Kaviya Maaran",email="kaviya@sun.com")
    db.session.add(buyer)
    db.session.commit()
    flash("Buyer added!",'success')

    return render_template('show.html',buyer=buyer)


@buyers.route('/buyers/show')
def show_buyers():
    buyers=Buyers.query.all()
    return render_template('show.html',buyers=buyers)



