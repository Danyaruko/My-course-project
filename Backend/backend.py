from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_serial import Serial
from flask_cors import CORS
from marshmallow_enum import EnumField
from marshmallow import fields, validate, exceptions
from state import State
from dotenv import load_dotenv
from datetime import datetime
import os


load_dotenv()

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
    user=str(os.getenv('user')),
    password=str(os.getenv('password')),
    host=str(os.getenv('host')),
    port=str(os.getenv('port')),
    database=str(os.getenv('database'))
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SERIAL_TIMEOUT'] = 0.2
app.config['SERIAL_PORT'] = 'COM3'
app.config['SERIAL_BAUDRATE'] = 9600
app.config['SERIAL_BYTESIZE'] = 8
app.config['SERIAL_PARITY'] = 'N'
app.config['SERIAL_STOPBITS'] = 1

db = SQLAlchemy(app)
ma = Marshmallow(app)
ser = Serial(app)
CORS(app)


class Tank_State(db.Model):
    __tablename__ = 'tank_state'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Enum(State))
    time = db.Column(db.DateTime)

    def __init__(self, state=State.EMPTY, time=datetime.now()):
        self.state = state
        self.time = time

    def update(self, state, time):
        self.__init__(state, time)


class Tank_StateSchema(ma.Schema):
    state = EnumField(State)

    class Meta:
        # Fields to expose
        fields = ('state', 'time')


tank_state_schema = Tank_StateSchema()
tank_states_schema = Tank_StateSchema(many=True)


@app.errorhandler(exceptions.ValidationError)
def handle_exception(e):
    return e.messages, 400

# endpoint to create new tank_state


@ser.on_message()
def handle_message(msg):
    float_state = msg
    print(float_state)
    print("receive a message:", msg)
    if float_state == b'\xa1':
        add_tank_state(State.FULL)
    if float_state == b'\xb1':
        add_tank_state(State.REFILLING)
    if float_state == b'\xc1':
        add_tank_state(State.EMPTY)


def add_tank_state(state):
    new_tank_state = Tank_State(state, datetime.now())

    db.session.add(new_tank_state)
    db.session.commit()

    return None


# endpoint to show all tank_states
@app.route("/tank_state", methods=["GET"])
def get_tank_state():
    all_tank_states = Tank_State.query.order_by(Tank_State.id.desc())
    result = tank_states_schema.dump(all_tank_states)
    return jsonify(result)


@app.route("/tank_state_last", methods=["GET"])
def get_last_tank_state():
    last_tank_states = Tank_State.query.order_by(Tank_State.id.desc()).limit(1)
    result = tank_states_schema.dump(last_tank_states)
    return jsonify(result)

# endpoint to get tank_state detail by id


# endpoint to get a teapot state code


@app.route("/teapot", methods=["GET"])
def teapot_detail():
    abort(418)
    return None


if __name__ == '__main__':
    app.run(debug=False)
