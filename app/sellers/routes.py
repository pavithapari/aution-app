from flask import Blueprint,render_template,session,flash,redirect,url_for,request
from app.models import Sellers,objects,Auction
from app import db
from app.sellers.forms import SellerReg_form,obj_form
sellers=Blueprint('sellers',__name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'seller':
            flash("Please login as seller", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@sellers.route('/seller/dashboard')
@login_required
def dashboard():
    return render_template("seller_dashboard.html")

@sellers.route('/seller/auctions')
@login_required
def my_auctions():
    user_id = session['user_id']
    auctions = Auction.query.filter_by(seller_id=user_id).all()
    return render_template("seller_auctions.html", auctions=auctions)

@sellers.route('/seller/auction/create', methods=['GET','POST'])
@login_required
def create_auction():
    # Implement form to create auction
    return render_template("seller_create_auction.html")

@sellers.route('/seller/auction/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit_auction(id):
    # Implement form to edit auction
    return f"Edit auction {id}"


@sellers.route('/seller/auction/<int:id>/close')
@login_required
def close_auction(id):
    auction = Auction.query.get_or_404(id)
    auction.status = "closed"
    db.session.commit()
    flash("Auction closed", "success")
    return redirect(url_for('sellers.my_auctions'))

@sellers.route('/sellers/register')
def register():
    form=SellerReg_form()
    if form.validate_on_submit():
        sellers=Sellers(username=form.name.data,email=form.email.data)
        db.session.add(sellers)
        db.session.commit()

    return render_template('seller_register.html',seller_form=form)


@sellers.route('/sellers/add-item',methods=['GET','POST'])
def add_item():
    form = obj_form()
    if form.validate_on_submit():
        object = objects(
            name=form.name.data,
            img=form.image.data,
            base_price=form.price.data,
            curr_price=form.price.data   # set current price same as base initially
        )
        db.session.add(object)
        db.session.commit()
        flash("The object has been added to the auction!", "info")
        return redirect(url_for('main.home'))
    return render_template('object_register.html', form=form)

@sellers.route('/sellers/edit-item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    object = objects.query.get_or_404(item_id)
    form = obj_form(obj=object)  # Pre-fill form with existing data

    if form.validate_on_submit():
        object.name = form.name.data
        object.img = form.image.data
        object.base_price = form.price.data
        object.curr_price = form.price.data  # You can choose to keep or update this

        db.session.commit()
        flash("The item has been updated successfully!", "success")
        return redirect(url_for('main.home'))

    return render_template('object_edit.html', form=form, object=object)

