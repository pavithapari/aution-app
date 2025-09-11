"""User

* `id
* `username`
* `email`
* `password_hash`
* `role` (`buyer`, `seller`, `admin`)
* `created_at`

---

Auction

* `id`
* `title`
* `description`
* `starting_price`
* `current_price`
* `image_url`
* `status` (`active`, `closed`, `cancelled`)
* `end_time`
* `seller_id` (FK → User.id)
* `winner_id` (FK → User.id, nullable)


Bid

* `id`
* `amount`
* `timestamp`
* `bidder_id` (FK → User.id)
* `auction_id` (FK → Auction.id)
"""
from app import db
from flask_login import UserMixin

class Buyers(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password=db.Column(db.String(120),nullable=False)



class Sellers(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)


class objects(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    img = db.Column(db.String(100))
    base_price = db.Column(db.Integer)
    curr_price = db.Column(db.Integer)
    no_of_people = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active')  # active or closed
    winner_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=True)  # store winner


