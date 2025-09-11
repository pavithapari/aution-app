from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from flask_socketio import emit, join_room
from app import socketio, db
from collections import defaultdict
from app.models import objects

bids = Blueprint('bids', __name__)

# Store auction state per item
auctions = defaultdict(lambda: {'highest_bid': 0, 'highest_bidder': None})

@bids.route('/bids/')
@login_required
def join_bid():
    item_id = request.args.get('item_id')
    auction_item = objects.query.get_or_404(item_id)

    # Initialize auction state
    if str(item_id) not in auctions:
        auctions[str(item_id)] = {
            'highest_bid': auction_item.curr_price or auction_item.base_price,
            'highest_bidder': None
        }

    return render_template(
        'bids.html',
        image=auction_item.img,
        item_id=item_id,
        current_user=current_user,
        initial_bid=auctions[str(item_id)]['highest_bid'],
        initial_bidder=auctions[str(item_id)]['highest_bidder']
    )

# ---------------- SOCKET.IO EVENTS ----------------

@socketio.on('joinAuction')
def handle_join(data):
    item_id = str(data['image_id'])
    join_room(item_id)
    emit('bidUpdate', {
        'item_id': item_id,
        'highest_bid': auctions[item_id]['highest_bid'],
        'highest_bidder': auctions[item_id]['highest_bidder']
    }, to=request.sid)

@socketio.on('newBid')
def handle_new_bid(data):
    item_id = str(data['image_id'])
    amount = int(data['amount'])
    username = data['username']

    auction_item = objects.query.get(int(item_id))
    if not auction_item or auction_item.status == 'closed':
        emit('bidRejected', 'Auction has ended.', to=request.sid)
        return

    current = auctions[item_id]
    if amount > current['highest_bid']:
        # Update auction state
        auctions[item_id]['highest_bid'] = amount
        auctions[item_id]['highest_bidder'] = username

        # Update database
        auction_item.curr_price = amount
        db.session.commit()

        # Broadcast update to all clients in this room (bidders + sellers)
        socketio.emit('bidUpdate', {
            'item_id': item_id,
            'highest_bid': amount,
            'highest_bidder': username
        }, room=item_id)
    else:
        emit('bidRejected', 'Bid must be higher than current highest.', to=request.sid)

@socketio.on('endAuction')
def handle_end_auction(data):
    item_id = str(data['image_id'])
    auction = auctions.get(item_id)

    auction_item = objects.query.get(int(item_id))
    if auction_item:
        auction_item.status = 'closed'
        db.session.commit()

    if auction:
        socketio.emit('auctionEnded', {
            'item_id': item_id,
            'winner': auction['highest_bidder'],
            'final_bid': auction['highest_bid']
        }, room=item_id)
