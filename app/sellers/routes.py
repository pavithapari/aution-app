from flask import Blueprint,render_template,flash
from app.models import Sellers
from app import db
from app.sellers.forms import SellerReg_form
sellers=Blueprint('sellers',__name__)


@sellers.route('/sellers/register')
def register():
    form=SellerReg_form()
    if form.validate_on_submit():
        sellers=Sellers(username=form.name.data,email=form.email.data)
        db.session.add(sellers)
        db.session.commit()

    return render_template('seller_register.html',seller_form=form)