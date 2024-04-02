from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()

        messages_dict = [message.to_dict() for message in messages]

        response = make_response(
            messages_dict,
            200
        )
        return response
    
    elif request.method == 'POST':
        form_data = request.get_json()

        try:
            new_message = Message(
                body = form_data['body'],
                username = form_data['username']
            )

            db.session.add(new_message)
            db.session.commit()

            response = make_response(
                new_message.to_dict(),
                201
            )

        
        except ValueError:
            response = make_response(
                { 'message' : 'put message here for for validation'},
                404
            )
            
            return response

        return response
        

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()

    if message:

        if request.method == 'GET':
            message_dict = message.to_dict()
            response = make_response(
                message_dict,
                200
            )

        elif request.method == 'PATCH':
            form_data = request.get_json()

            for attr in form_data:
                setattr(message, attr, form_data.get(attr))

                db.session.commit()

                response = make_response(
                    message.to_dict(),
                    201
                )

        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response = make_response(
                {},
                202
            )
            
    else:
        response = make_response(
            { "Message not found!": None },
            404
        )
    return response

if __name__ == '__main__':
    app.run(port=5555)
