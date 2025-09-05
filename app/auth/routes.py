from flask import Blueprint,render_template,redirect,url_for,flash,session
from app.models import User
from app.auth.forms import LoginForm

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.Validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id']=user.id
            session['role']=user.role
            flash("logged in successfully","success")
            if user.role=='buyer':
                return redirect(url_for('buyers.dashboard'))
            else:
                return redirect(url_for('sellers.dashboard'))
        else:
            flash("Invalid email or password","danger")
    return render_template("login.html",form=form)
@auth.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully","success")
    return redirect(url_for('main.home'))