from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'instance', 'reviews.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    rate = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Review {self.id}: {self.rate} stars'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('review_text', '').strip()
        rate = request.form.get('review_rate')
        
        if text and rate and rate.isdigit() and 1 <= int(rate) <= 5:
            db.session.add(Review(text=text, rate=int(rate)))
            db.session.commit()
            return redirect(url_for('index'))
    
    reviews = Review.query.order_by(Review.id.desc()).all()
    return render_template('index.html', reviews=reviews)

@app.route('/clear', methods=['POST'])
def clear_reviews():
    try:
        deleted = db.session.query(Review).delete()
        db.session.commit()
        print(f"Deleted {deleted} reviews")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
    return redirect(url_for('index'))

def create_app():
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)