import hashlib
import time

from flask import abort, Flask, jsonify, render_template, request

from config import SECRET_KEY
from models import db, Data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

@app.route('/')
def show_index_page():
    return render_template('index.html')

@app.route('/<username>')
def show_user_profile(username):
    # show the user profile for that user
    user = Data.query.filter_by(username=username).first()

    if user:
        return render_template('profile.html', username=user.username, battery_percent=user.battery_percent, status=user.status)
    else:
        abort(404)

@app.route('/update')
def update_user_profile():
    username = request.args.get('username')
    battery_percent = request.args.get('battery_percent')
    request_key = request.args.get('key')
    status = request.args.get('status')
    status_last_updated = time.strftime("%d:%m:%Y:%H:%M:%S")

    ret_json = {}

    if request_key == hashlib.md5(username + time.strftime("%d:%m:%Y:%H:%M") + SECRET_KEY).hexdigest():
        # show the user profile for that user
        user = Data.query.filter_by(username=username).first()

        try:
            if user:
                user.battery_percent = battery_percent
                if status:
                    user.status = status
                    user.status_last_updated = status_last_updated
                db.session.commit()
                ret_json["message"] = "Successfully updated"
                ret_json["code"] = 200
            else:
                user = Data(username, battery_percent, status, status_last_updated)
                db.session.add(user)
                db.session.commit()
                ret_json["message"] = "Successfully created"
                ret_json["code"] = 200
        except:
            ret_json["message"] = "Error updating user profile"
            ret_json["code"] = 500
    else:
        ret_json["message"] = "Key mismatch"
        ret_json["code"] = 403
    return jsonify(ret_json)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)