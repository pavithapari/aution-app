from flask import render_template,request
from flask import Flask
from flask import Blueprint


main=Blueprint('main', __name__)

@main.route('/home')
def home():
    return render_template('base.html')



