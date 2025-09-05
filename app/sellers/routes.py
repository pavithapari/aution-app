from flask import Blueprint,render_template,flash,redirect,url_for
from app.models import Sellers,objects
from app import db
from app.sellers.forms import SellerReg_form,obj_form
sellers=Blueprint('sellers',__name__)


@sellers.route('/sellers/register')
def register():
    form=SellerReg_form()
    if form.validate_on_submit():
        sellers=Sellers(username=form.name.data,email=form.email.data)
        db.session.add(sellers)
        db.session.commit()

    return render_template('seller_register.html',seller_form=form)


@sellers.route('/sellers/add-item',methods=['GET','POST'])
def add_item():
    form = obj_form()
    if form.validate_on_submit():
        object = objects(
            name=form.name.data,
            img=form.image.data,
            base_price=form.price.data,
            curr_price=form.price.data   # set current price same as base initially
        )
        db.session.add(object)
        db.session.commit()
        flash("The object has been added to the auction!", "info")
        return redirect(url_for('main.home'))
    return render_template('object_register.html', form=form)

@sellers.route('/sellers/edit-item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    object = objects.query.get_or_404(item_id)
    form = obj_form(obj=object)  # Pre-fill form with existing data

    if form.validate_on_submit():
        object.name = form.name.data
        object.img = form.image.data
        object.base_price = form.price.data
        object.curr_price = form.price.data  # You can choose to keep or update this

        db.session.commit()
        flash("The item has been updated successfully!", "success")
        return redirect(url_for('main.home'))

    return render_template('object_edit.html', form=form, object=object)

