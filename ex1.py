import datetime
import os
from sqlalchemy import String, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_dir =  'sqlite:///' + os.path.join(BASE_DIR, 'company1.db')

engine = create_engine(db_dir, echo=False)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

    
class Employee(Base):
    
    __tablename__ = 'employee'

    id = Column(Integer,primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(32))
    
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
    
session.commit()

myemployees = session.query(Employee).order_by(Employee.id)
for person in myemployees:
    print person.first_name, person.last_name
    
    

    