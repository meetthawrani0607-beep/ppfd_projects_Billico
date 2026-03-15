from app_demo import app
from models import db
from models.user import User

with app.app_context():
    # Check if demo user already exists
    if not User.query.filter_by(email='demo@billico.com').first():
        user = User(
            username='demo_user',
            email='demo@billico.com',
            password='demo123',
            full_name='Demo User'
        )
        db.session.add(user)
        db.session.commit()
        print("Demo user created successfully!")
    else:
        print("Demo user already exists.")
