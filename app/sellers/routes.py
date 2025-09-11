from flask import Blueprint,render_template,flash,redirect,url_for
from app.models import Sellers,objects,Buyers
from app import db,socketio
from app.sellers.forms import SellerReg_form,obj_form,SellerLog_form
from app.bids.routes import auctions
sellers=Blueprint('sellers',__name__)


@sellers.route('/sellers/register',methods=['GET','POST'])
def register():
    form=SellerReg_form()
    if form.validate_on_submit():
        sellers=Sellers(username=form.name.data,email=form.email.data)
        db.session.add(sellers)
        db.session.commit()
        return redirect(url_for('sellers.login'))

    return render_template('seller_register.html',seller_form=form)

@sellers.route('/sellers/login',methods=['GET','POST'])
def login():
    form=SellerLog_form()
    if form.validate_on_submit():
        seller=Sellers.query.filter_by(email=form.email.data).first()
        if seller:
            # login_user(seller)  # Uncomment if using Flask-Login
            return redirect(url_for('sellers.home'))
        flash("Wrong mail or password or both",'danger')
        return redirect(url_for('sellers.login'))
    return render_template('seller_login.html',seller_form=form)

@sellers.route('/sellers/home')
def home():
    all_items = objects.query.all()
    return render_template('seller_dashboard.html', items=all_items)

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
    form = obj_form(obj=object)  

    if form.validate_on_submit():
        object.name = form.name.data
        object.img = form.image.data
        object.base_price = form.price.data
        object.curr_price = form.price.data  

        db.session.commit()
        flash("The item has been updated successfully!", "success")
        return redirect(url_for('main.home'))

    return render_template('object_edit.html', form=form, object=object)


@sellers.route('/sellers/end-auction/<int:item_id>', methods=['POST'])
def end_auction(item_id):
    object = objects.query.get_or_404(item_id)
    
    if object.status == 'closed':
        flash("Auction is already closed.", "info")
        return redirect(url_for('sellers.home'))

    object.status = 'closed'

    # Determine winner
    auction_state = auctions.get(str(object.id))
    if auction_state and auction_state.get('highest_bidder'):
        object.curr_price = auction_state['highest_bid']
        # Get buyer object by username
        winner = Buyers.query.filter_by(username=auction_state['highest_bidder']).first()
        if winner:
            object.winner_id = winner.id
    db.session.commit()

    # Emit event to notify all bidders that auction ended
    socketio.emit('auctionEnded', {
        'winner': auction_state.get('highest_bidder') if auction_state else None,
        'final_bid': auction_state.get('highest_bid') if auction_state else None,
        'item_id': object.id
    })

    flash(f"Auction for '{object.name}' has been ended.", "success")
    return redirect(url_for('sellers.home'))



