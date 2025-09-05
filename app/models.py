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
from werkzeug.security import generate_password_hash,check_password_hash
from app import db


class Buyers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)



class Sellers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    email=db.Column(db.String(120),nullable=False,unique=True)
    password_hash=db.Column(db.tString(128),nullable=False)
    role=db.Column(db.String(10),nullable=False)


    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)