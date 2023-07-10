from flask import Flask, request, jsonify
from flask_validators import validate_form, Schema, Field, DataValidator, validate_db
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Set up the Flask application
app = Flask(__name__)

# Set up the SQLite database
database_url = 'sqlite:///test_database.db'
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)

# Define the User model
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)

# Create the database tables
Base.metadata.create_all(engine)

# Delete any existing records from the users table
Base.metadata.drop_all(engine, tables=[User.__table__])
Base.metadata.create_all(engine)

# Add a test record to the database
session = Session()
user = User(username='testuser', email='test@example.com')
session.add(user)
session.commit()

# Define the Flask routes
@app.route('/validate', methods=['POST'])
@validate_db(User, Session, ['email'])
def validate_data():
    return jsonify({'success': True, 'message': 'Data is valid.'})

if __name__ == '__main__':
    app.run(debug=True)