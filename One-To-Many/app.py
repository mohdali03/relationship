from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_NOTIFICATION']=False

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    notes=db.relationship('Notes',backref='user')

    def __repr__(self) -> str:
        return f"<User:{self.name}>"


class Notes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    note=db.Column(db.String(20))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id', ondelete="CASCADE")
    )
 
    def __repr__(self) -> str:
        return f"<Note:{self.note}>"
    
    
with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
        data = request.get_json()
        new_user = User(name=data['name'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'name': user.name})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.name = data['name']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    new_note = Notes(note=data['note'], user_id=data['user_id'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note created successfully'}), 201

@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Notes.query.all()
    return jsonify([{'id': note.id, 'note': note.note, 'user_id': note.user_id} for note in notes])

@app.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Notes.query.get_or_404(id)
    return jsonify({'id': note.id, 'note': note.note, 'user_id': note.user_id})

@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.get_json()
    note = Notes.query.get_or_404(id)
    note.note = data['note']
    db.session.commit()
    return jsonify({'message': 'Note updated successfully'})

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Notes.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'})

if __name__=="__main__":
    app.run(debug=True)
    