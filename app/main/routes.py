from flask import render_template,request
from flask import Flask
from flask import Blueprint


main=Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')



