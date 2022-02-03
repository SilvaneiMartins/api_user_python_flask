from flask import Flask, jsonify, request, make_response, abort

from database import db
from models.users import USERS, USERSEncoder

app = Flask(__name__)
app.config['DEBUG'] = True
app.json_encoder = USERSEncoder


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Status': 404, 'Error': 'Resource not found'}), 404)


@app.route('/api/v1/resorces/home', methods=['GET'])
def home():
    return '<h1>Silvanei Martins</h1>'


@app.route('/api/v1/resorces/users', methods=['GET'])
def lists():
    return jsonify({'users': db})


@app.route('/api/v1/resorces/users/<int:id>', methods=['GET'])
def list(id):
    for user in db:
        if id == user.id:
            return jsonify(user)
    abort(404)


@app.route('/api/v1/resorces/users', methods=['POST'])
def create():
    if not request.json or not "name" in request.json:
        abort(404)
    user = USERS(request.json['name'],
                 request.json['email'],
                 request.json['password'],
                 )
    db.append(user)
    return jsonify(user), 201


@app.route('/api/v1/resorces/users/<int:id>', methods=['PUT'])
def update(id):
    if not request.json:
        abort(404)
    for user in db:
        if user.id == id:
            user.name = request.json['name']
            user.email = request.json['email']
            user.passwrod = request.json['password']
            return jsonify({'Atualizado com sucesso!': True})
    abort(404)


@app.route('/api/v1/resorces/users/<int:id>', methods=['DELETE'])
def delete(id):
    for user in db:
        if user.id == id:
            db.remove(user)
            return jsonify({"Usuário excluído com sucesso!": True})
    abort(404)


app.run()
