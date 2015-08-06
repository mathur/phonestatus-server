from flask import abort, Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    battery_percent = db.Column(db.Integer)
    status = db.Column(db.Text)

    def __init__(self, username, battery_percent, status):
        self.username = username
        self.battery_percent = battery_percent
        self.status = status

    def __repr__(self):
        return '<Data for %r>' % self.username

@app.route('/<username>')
def show_user_profile(username):
    # show the user profile for that user
    user = Data.query.filter_by(username=username).first()

    if user:
        return render_template('profile.html', username=username)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)