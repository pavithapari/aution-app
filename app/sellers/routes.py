from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from app.models import Sellers, objects, Buyers
from app import db, socketio
from app.sellers.forms import SellerReg_form, obj_form, SellerLog_form
from app.bids.routes import auctions

sellers = Blueprint('sellers', __name__)

# ------------------ REGISTER ------------------
@sellers.route('/sellers/register', methods=['GET', 'POST'])
def register():
    form = SellerReg_form()
    if form.validate_on_submit():
        seller = Sellers(username=form.name.data, email=form.email.data)
        db.session.add(seller)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('sellers.login'))
    return render_template('seller_register.html', seller_form=form)

# ------------------ LOGIN ------------------
@sellers.route('/sellers/login', methods=['GET', 'POST'])
def login():
    form = SellerLog_form()
    if form.validate_on_submit():
        seller = Sellers.query.filter_by(email=form.email.data).first()
        if seller:
            session['seller_id'] = seller.id
            flash("Logged in successfully.", "info")
            return redirect(url_for('sellers.home'))
        flash("Wrong email or password.", "danger")
        return redirect(url_for('sellers.login'))
    return render_template('seller_login.html', seller_form=form)

# ------------------ LOGOUT ------------------
@sellers.route('/sellers/logout')
def logout():
    session.pop('seller_id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('main.index'))

# ------------------ DASHBOARD ------------------
@sellers.route('/sellers/home')
def home():
    if 'seller_id' not in session:
        flash("Please log in to access your dashboard.", "warning")
        return redirect(url_for('sellers.login'))

    seller_items = objects.query.filter_by(seller_id=session['seller_id']).all()
    return render_template('seller_dashboard.html', items=seller_items, Buyers=Buyers)

# ------------------ ADD ITEM ------------------
@sellers.route('/sellers/add-item', methods=['GET', 'POST'])
def add_item():
    if 'seller_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('sellers.login'))

    form = obj_form()
    if form.validate_on_submit():
        object = objects(
            name=form.name.data,
            img=form.image.data,
            base_price=form.price.data,
            curr_price=form.price.data,
            seller_id=session['seller_id']
        )
        db.session.add(object)
        db.session.commit()
        flash("The object has been added to the auction!", "info")
        return redirect(url_for('sellers.home'))
    return render_template('object_register.html', form=form)

# ------------------ EDIT ITEM ------------------
@sellers.route('/sellers/edit-item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'seller_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('sellers.login'))

    object = objects.query.get_or_404(item_id)
    if object.seller_id != session['seller_id']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('sellers.home'))

    form = obj_form(obj=object)
    if form.validate_on_submit():
        object.name = form.name.data
        object.img = form.image.data
        object.base_price = form.price.data
        object.curr_price = form.price.data
        db.session.commit()
        flash("The item has been updated successfully!", "success")
        return redirect(url_for('sellers.home'))
    return render_template('object_edit.html', form=form, object=object)

# ------------------ DELETE ITEM ------------------
@sellers.route('/sellers/delete-item/<int:item_id>', methods=['POST', 'GET'])
def delete_item(item_id):
    if 'seller_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('sellers.login'))

    object = objects.query.get_or_404(item_id)
    if object.seller_id != session['seller_id']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('sellers.home'))

    db.session.delete(object)
    db.session.commit()
    flash("The item has been deleted successfully!", "info")
    return redirect(url_for('sellers.home'))

# ------------------ END AUCTION ------------------
@sellers.route('/sellers/end-auction/<int:item_id>', methods=['POST'])
def end_auction(item_id):
    if 'seller_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('sellers.login'))

    object = objects.query.get_or_404(item_id)
    if object.seller_id != session['seller_id']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('sellers.home'))

    if object.status == 'closed':
        flash("Auction is already closed.", "info")
        return redirect(url_for('sellers.home'))

    object.status = 'closed'
    auction_state = auctions.get(str(object.id))
    if auction_state and auction_state.get('highest_bidder'):
        object.curr_price = auction_state['highest_bid']
        winner = Buyers.query.filter_by(username=auction_state['highest_bidder']).first()
        if winner:
            object.winner_id = winner.id
    db.session.commit()

    socketio.emit('auctionEnded', {
        'winner': auction_state.get('highest_bidder') if auction_state else None,
        'final_bid': auction_state.get('highest_bid') if auction_state else None,
        'item_id': object.id
    })

    flash(f"Auction for '{object.name}' has been ended.", "success")
    return redirect(url_for('sellers.home'))