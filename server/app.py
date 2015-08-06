from flask import abort, Flask, render_template

from models import db, Data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

@app.route('/<username>')
def show_user_profile(username):
    # show the user profile for that user
    user = Data.query.filter_by(username=username).first()

    if user:
        return render_template('profile.html', username=username)
    else:
        abort(404)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)