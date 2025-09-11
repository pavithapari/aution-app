from flask import Blueprint, render_template, request
from flask_login import current_user,login_required
from flask_socketio import emit
from app import socketio
from collections import defaultdict
from app.models import objects

bids = Blueprint('bids', __name__)

# Store auction state per image
auctions = defaultdict(lambda: {'highest_bid': 0, 'highest_bidder': None})


@bids.route('/bids/')
@login_required
def join_bid():
    item_id = request.args.get('item_id')  # pass item ID in URL
    auction_item = objects.query.get_or_404(item_id)

    # Get current highest bid and bidder from auctions dict
    auction_state = auctions.get(str(item_id), {'highest_bid': auction_item.curr_price, 'highest_bidder': None})
    initial_bid = auction_state['highest_bid']
    initial_bidder = auction_state['highest_bidder']

    return render_template(
        'bids.html',
        image=auction_item.img,
        item_id=item_id,
        current_user=current_user,
        initial_bid=initial_bid,
        initial_bidder=initial_bidder
    )

@socketio.on('joinAuction')
def handle_join(data):
    image_id = data['image_id']
    emit('bidUpdate', auctions[image_id])

@socketio.on('newBid')
def handle_new_bid(data):
    image_id = data['image_id']
    amount = int(data['amount'])
    username = data['username']

    auction_item = objects.query.get(image_id)
    if not auction_item or auction_item.status == 'closed':
        emit('bidRejected', 'Auction has ended.')
        return

    current = auctions[image_id]
    if amount > current['highest_bid']:
        auctions[image_id]['highest_bid'] = amount
        auctions[image_id]['highest_bidder'] = username
        emit('bidUpdate', auctions[image_id])
    else:
        emit('bidRejected', 'Bid must be higher than current highest.')


