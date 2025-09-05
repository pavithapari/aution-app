from flask import render_template,redirect,url_for
from flask import Flask
from flask import Blueprint
from app.models import objects,db


main=Blueprint('main', __name__)
@main.route('/')
def home():
    # Get the most popular item based on number of bidders
    top = objects.query.order_by(objects.no_of_people.desc()).first()

    # Get all items for display
    all_items = objects.query.all()

    return render_template('home.html', top=top, obj=all_items)

@main.route('/delete')
def delete():
    db.drop_all()
    return redirect(url_for('main.home'))





