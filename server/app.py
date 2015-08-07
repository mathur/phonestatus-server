from flask import abort, Flask, jsonify, render_template, request

from models import db, Data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

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
    status = request.args.get('status')

    ret_json = {
        "message": "",
        "code": "",
    }

    # show the user profile for that user
    user = Data.query.filter_by(username=username).first()

    if user:
        user.battery_percent = battery_percent
        if status:
            user.status = status
        db.session.commit()
        ret_json["message"] = "Successfully updated"
        ret_json["code"] = 200
    else:
        user = Data(username, battery_percent, status)
        db.session.add(user)
        db.session.commit()
        ret_json["message"] = "Successfully created"
        ret_json["code"] = 200
    return jsonify(ret_json)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)