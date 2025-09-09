import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for, jsonify, abort,Blueprint
from flask_socketio import  join_room, leave_room, emit
from app import db,socketio
from app.models import objects

online_users = {}  
bids=Blueprint('bids',__name__)


@bids.route("/auction/<int:item_id>")
def auction_room(item_id):
    item = objects.query.get_or_404(item_id)
    return render_template("auction_room.html", item=item)



@socketio.on("join_auction")
def handle_join_auction(data):
    room = f"auction_{data['item_id']}"
    join_room(room)
    emit("system_message", {
        "text": f"{data['username']} joined auction room.",
        "timestamp": datetime.utcnow().isoformat()
    }, room=room)

@socketio.on("place_bid")
def handle_place_bid(data):
    item = objects.query.get(data["item_id"])
    amount = float(data["amount"])
    username = data["username"]

    if not item or amount <= item.curr_price:
        emit("bid_error", {"message": "Bid must be higher than current price."}, room=f"auction_{item.id}")
        return

    item.curr_price = amount
    db.session.commit()
    emit("new_bid", {
        "username": username,
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat()
    }, room=f"auction_{item.id}")
