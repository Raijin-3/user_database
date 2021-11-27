from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city =  db.Column(db.String(200), nullable=False)
    
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
    
    
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/all')
def get_all_users():
    users = db.session.query(User).all()
    return jsonify( users = [user.to_dict()  for user in users] )


@app.route('/search', methods = ['GET'])
def find_user_by_city():
    query_city = request.args.get("city")
    user = db.session.query(User).filter_by(city = query_city).first()
    if user:
        return jsonify(user = user.to_dict())
    else:
        return jsonify(error = {"Not Found" : "Sorry, we do not have any user at that city"}),404
    
    
@app.route('/add', methods=['POST'])
def post_new_user():
    new_user = User(
        name = request.form.get('name'),
        age = request.form.get('age'),
        city = request.form.get('city')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify (response = {"success" : "Successfully added the new user"} ),200


@app.route('/update-user/<int:user_id>', methods = ["PATCH"])
def patch_user(user_id):
    new_city = request.args.get("new_city")
    user = db.session.query(User).get(user_id)
    if user:
        user.city = new_city
        db.session.commit()
        return jsonify(response={"success":"Successfully updated to new city"}), 200
    else:
        return jsonify(response={"Not Found": "A user with that id was not found"}),404
    
    
@app.route('/user_delelted/<int:user_id>', methods = ["DELETE"])
def delete_user(user_id):
    api_key = request.args.get("api-key")
    if api_key == "HappyThanksGivingAlthoughIAmNotAmerican":
        user = db.session.query(User).get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(response = {"success":"Successfully deleted the user"}),200
        else:
            return jsonify(error = {"Not Found": "A user with that id is not found"}),404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
            


if __name__ == '__main__':
    app.run(debug=True)