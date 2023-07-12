from flask import Flask, request, jsonify
from flask_validators import validate_form, Schema, Field, DataValidator, validate_db, validate_llm
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

database_url = 'sqlite:///test_database.db'
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)

Base.metadata.create_all(engine)

Base.metadata.drop_all(engine, tables=[User.__table__])
Base.metadata.create_all(engine)

session = Session()
user1 = User(username='testuser1', email='test1@example.com')
user2 = User(username='testuser2', email='test2@example.com')
session.add(user1)
session.add(user2)
session.commit()

@app.route('/check_unique', methods=['POST'])
@validate_db(User, Session, email=['check_unique'])
def check_unique_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})

@app.route('/check_null', methods=['POST'])
@validate_db(User, Session, username=['check_null'])
def check_null_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})

@app.route('/check_existence', methods=['POST'])
@validate_db(User, Session, id=['check_existence'])
def check_existence_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})

@app.route('/check_range', methods=['POST'])
@validate_db(User, Session, username=['check_range'])
def check_range_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})

@app.route('/check_type', methods=['POST'])
@validate_db(User, Session, username=['check_type'])
def check_type_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})

@app.route('/check_enum', methods=['POST'])
@validate_db(User, Session, status=['check_enum'])
def check_enum_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})

@app.route('/check_length', methods=['POST'])
@validate_db(User, Session, username=['check_length'])
def check_length_endpoint():
    return jsonify({'success': True, 'message': 'Data is valid.'})

@app.route('/check_form', methods=['POST'])
@validate_form('name', 'age')
def check_form():
    return jsonify({'success': True, 'message': 'Data is valid.'})

@app.route('/validate_language', methods=['POST'])
@validate_llm(text=['validate_language'], lang='ka')
def validate_lang():
    return jsonify({'success': True, 'message': 'Data is valid.'})

if __name__ == '__main__':
    app.run(debug=True)