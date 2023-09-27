from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Use SQLite as an example database
db = SQLAlchemy(app)


# Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    start = db.Column(db.String(1000))
    end = db.Column(db.String(1000))
    url = db.Column(db.String(1000))

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    events = Event.query.all()
    return render_template('home.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        url = request.form['url']
        if end == '':
            end = start
        new_event = Event(title=title, start=start, end=end, url=url)
        db.session.add(new_event)
        db.session.commit()
    return render_template('add.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        event_id = request.form['event']
        event_to_remove = Event.query.get(event_id)
        if event_to_remove:
            db.session.delete(event_to_remove)
            db.session.commit()
    events = Event.query.all()
    return render_template('remove.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)
