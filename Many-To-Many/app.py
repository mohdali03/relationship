from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db=SQLAlchemy(app)

user_page=db.Table('user_page',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('page_id',db.Integer,db.ForeignKey('page.id')),
)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    following=db.relationship('Page',secondary=user_page,backref='followers')

    def __repr__(self) -> str:
        return f'<User:{self.name}>'

class Page(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))

    def __repr__(self) -> str:
        return f'<page:{self.name}>'

    
with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

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

@app.route('/pages', methods=['POST'])
def create_page():
    data = request.get_json()
    new_page = Page(name=data['name'])
    db.session.add(new_page)
    db.session.commit()
    return jsonify({'message': 'Page created successfully'}), 201

@app.route('/pages/<int:id>', methods=['GET'])
def get_page(id):
    page = Page.query.get_or_404(id)
    return jsonify({'id': page.id, 'name': page.name})

@app.route('/pages/<int:id>', methods=['PUT'])
def update_page(id):
    data = request.get_json()
    page = Page.query.get_or_404(id)
    page.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Page updated successfully'})

@app.route('/pages/<int:id>', methods=['DELETE'])
def delete_page(id):
    page = Page.query.get_or_404(id)
    db.session.delete(page)
    db.session.commit()
    return jsonify({'message': 'Page deleted successfully'})

if __name__=="__main__":
    app.run(debug=True)