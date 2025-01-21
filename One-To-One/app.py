from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///my.db"
app.config['SQLALCHEMY_TRACK_NOTIFICATION']=False
# One-To-Many
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    profile=db.relationship('Profile',backref='user', uselist=False)

    def __repr__(self) -> str:
        return f"<User:{self.name}>"
    
with app.app_context():
    db.create_all()

class Profile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id', ondelete="CASCADE"), unique=True)
 
    def __repr__(self) -> str:
        return f"<Profie:{self.username}>"
    
    
    
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({"id": user.id, "name": user.name})

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.name = data['name']
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

if __name__=="__main__":
    app.run(debug=True)