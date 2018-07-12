from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os 

test_app = Flask('test_app')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'company.db')
test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#metadata = MetaData(schema='myschema')
db = SQLAlchemy(test_app)




    
    
class Employee(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(32))
    
    def __init__(self, first_name, last_name, gender):
        self.first_name  = first_name
        self.last_name = last_name
        self.gender = gender
        

    def __repr__(self):
        return '<Employee %s %s>' % (self.first_name, self.last_name)
    
    
    
db.create_all()


employees = [
    Employee("Joe", "Smith", "Male"),
    Employee("Jill", "Williams", "Female"),
    Employee("John", "Doe", "Male")
]    

    
for employee in employees:
    db.session.add(employee)
    
db.session.commit()

myemployees = Employee.query.all()
for person in myemployees:
    print person.first_name, person.last_name
    

    
import csv
with open("employees.csv", "r") as csvfile:
    data = csv.reader(csvfile, delimiter=",")
    for row in data:
        new_employee  = Employee(row[0], row[1], row[2])
        db.session.add(new_employee)
        
    db.session.commit()
    
myemployees = Employee.query.all()
for person in myemployees:
    print person.first_name, person.last_name
    