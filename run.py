from app import create_app,db
app=create_app()

with app.app_context():
    db.create_all()
"""To ckeck the changes"""

if __name__=="__main__":
    app.run(debug=True)