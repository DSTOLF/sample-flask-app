from models import db, Models, app

with app.app_context():
    # Reload tables
    db.drop_all()
    db.create_all()
