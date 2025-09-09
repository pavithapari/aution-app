from flask import render_template,redirect,url_for,request,session
from flask import Flask
from flask import Blueprint
from app.models import objects,db


main=Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        role = request.form['role']
        session['role'] = role
        return redirect(f'/{role}/home')
    return render_template('index.html')
@main.route('/buyers/home')
def home():
    top = objects.query.order_by(objects.no_of_people.desc()).first()
    all_items = objects.query.all()

    return render_template('home.html', top=top, obj=all_items)

@main.route('/delete')
def delete():
    db.drop_all()
    return redirect(url_for('main.home'))





