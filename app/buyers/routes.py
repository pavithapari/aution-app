"""WE can have routes for buyers related routes like their dashboards"""
from flask import Blueprint,render_template,flash,redirect,url_for
from app.models import Buyers
from flask_login import login_user,logout_user
from app import db,bcrypt
from app.buyers.forms import BuyerReg_form,BuyerLog_form
buyers=Blueprint('buyers',__name__)


@buyers.route('/buyers/register',methods=['GET','POST'])
def register():
    form=BuyerReg_form()
    if form.validate_on_submit():
        buyer=Buyers(username=form.name.data,email=form.email.data,password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(buyer)
        db.session.commit()
        return redirect(url_for('buyers.login'))

    return render_template('buyer_register.html',buyer_form=form)

@buyers.route('/buyers/login',methods=['GET','POST'])
def login():
    form=BuyerLog_form()
    if form.validate_on_submit():
        buyer=Buyers.query.filter_by(email=form.email.data).first()
        if buyer and bcrypt.check_password_hash(buyer.password,form.password.data):
            login_user(buyer)
            return redirect(url_for('main.home'))
        flash("Wrong mail or password or both",'danger')
        return redirect(url_for('buyers.login'))
    return render_template('buyer_login.html',form=form)


@buyers.route('/buyers/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@buyers.route('/buyers/show')
def show_buyers():
    buyers=Buyers.query.all()
    return render_template('show.html',buyers=buyers)



