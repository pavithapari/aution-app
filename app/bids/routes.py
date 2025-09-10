from flask import Blueprint, render_template, request
from flask_login import current_user,login_required
from flask_socketio import emit
from app import socketio
from collections import defaultdict

bids = Blueprint('bids', __name__)

# Store auction state per image
auctions = defaultdict(lambda: {'highest_bid': 0, 'highest_bidder': None})



@bids.route('/bids/')
@login_required
def join_bid():
    image = request.args.get('image')
    print(f"Curent user: {current_user} ")
    return render_template('bids.html', image=image,current_user=current_user)

@socketio.on('joinAuction')
def handle_join(data):
    image_id = data['image_id']
    emit('bidUpdate', auctions[image_id])

@socketio.on('newBid')
def handle_new_bid(data):
    image_id = data['image_id']
    amount = int(data['amount'])
    username = data['username']

    current = auctions[image_id]
    if amount > current['highest_bid']:
        auctions[image_id]['highest_bid'] = amount
        auctions[image_id]['highest_bidder'] = username
        emit('bidUpdate', auctions[image_id], broadcast=True)
    else:
        emit('bidRejected', 'Bid must be higher than current highest.')