import datetime
import os
import csv

from sqlalchemy import String, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_dir =  'sqlite:///' + os.path.join(BASE_DIR, 'company3.db')

engine = create_engine(db_dir, echo=False)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define a base model for other database tables to inherit
class Template(Base):

    __abstract__    = True

    id              = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())
    
class Employee(Template):
    
    __tablename__ = 'employee'

    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(32))
    role = "Employee"
    
    def __init__(self, first_name, last_name, gender):
        self.first_name  = first_name
        self.last_name = last_name
        self.gender = gender
        

    def __repr__(self):
        return '<Employee %s %s>' % (self.first_name, self.last_name)
    
    
class Manager(Template):
    
    __tablename__ = 'manager'

    #id = Column(Integer,primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(32))
    role = "Manager"
    
    def __init__(self, first_name, last_name, gender):
        self.first_name  = first_name
        self.last_name = last_name
        self.gender = gender
        

    def __repr__(self):
        return '<Employee %s %s>' % (self.first_name, self.last_name)
    
    

    
    
#print Employee.__table__
Base.metadata.create_all(engine)
    

session.add_all([Employee("Joe", "Smith", "Male"),
                 Employee("Jill", "Williams", "Female"),
                 Employee("John", "Doe", "Male")]
                )
    

session.add_all([Manager("Billy", "Bob", "Male"),
                 Manager("Jamie", "Jules", "Female"),
                 Manager("Leila", "Lulips", "Male")]
                )


session.commit()

myemployees = session.query(Employee).order_by(Employee.id)
for person in myemployees:
    print person.first_name, person.last_name, person.role
    
    
mymanagers = session.query(Manager).order_by(Manager.id)
for person in mymanagers:
    print person.first_name, person.last_name, person.role
    
    