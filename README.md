# SQLAlchemy ORM with Python

__Step 1:__

For this tutorial we will use a local SQLite database. To connect we use create_engine(). We are going to set the path of our database to the current folder.

Here we set the echo flag to True. If enabled, we’ll see all the generated SQL produced. 


```python
import os
from sqlalchemy import create_engine

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_dir =  'sqlite:///' + os.path.join(BASE_DIR, 'company1.db')
engine = create_engine(db_dir, echo=True)
```

The return value of create_engine() is an instance of `Engine` , and it represents the core interface to the database.  In this case the SQLite dialect will interpret instructions to the Python built-in sqlite3 module.

The Engine, when first returned by create_engine(), has not actually tried to connect to the database yet; that happens only the first time it is asked to perform a task against the database

__Step 2: Declare a Mapping__

When using the ORM, the configurational process starts by describing the database tables we’ll be dealing with, and then by defining our own classes which will be mapped to those tables.  

Classes mapped using the Declarative system are defined in terms of a base class which maintains a catalog of classes and tables relative to that base - this is known as the declarative base class. Our application will usually have just one instance of this base in a commonly imported module. We create the base class using the declarative_base() function, as follows:


```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

```

__Step 3:__

Now that we have a “base”, we can define any number of mapped classes in terms of it. We will start with just a single table called employees, which will store records for the end-users using our application. A new class called `Employee` will be the class to which we map this table. Within the class, we define details about the table to which we’ll be mapping, primarily the table name, and names and datatypes of columns:

```python
from sqlalchemy import String, Column, Integer, DateTime


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
```


A class using Declarative at a minimum needs a `__tablename__` attribute, and at least one Column which is part of a primary key [1]. SQLAlchemy never makes any assumptions by itself about the table to which a class refers, including that it has no built-in conventions for names, datatypes, or constraints.

When our class is constructed, Declarative replaces all the Column objects with special Python accessors known as descriptors; this is a process known as instrumentation. The “instrumented” mapped class will provide us with the means to refer to our table in a SQL context as well as to persist and load the values of columns from the database.




__Step 4: Create a Schema__

```python
#print Employee.__table__
Base.metadata.create_all(engine)

The MetaData is a registry which includes the ability to emit a limited set of schema generation commands to the database. As our SQLite database does not actually have a employees table present, we can use MetaData to issue CREATE TABLE statements to the database for all tables that don’t yet exist. Below, we call the MetaData.create_all() method, passing in our Engine as a source of database connectivity.

```

__Step 5: Create an Instance of the Mapped Class__

```python
session.add_all([Employee("Joe", "Smith", "Male"),
                 Employee("Jill", "Williams", "Female"),
                 Employee("John", "Doe", "Male")]
                )    
```

Even though we didn’t specify it in the constructor, the id attribute still produces a value of None when we access it (as opposed to Python’s usual behavior of raising AttributeError for an undefined attribute)

__Step 6: Creating a Session__

The ORM’s “handle” to the database is the Session. When we first set up the application, at the same level as our create_engine() statement, we define a Session class which will serve as a factory for new Session objects:

```python
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()
```
The above Session is associated with our SQLite-enabled Engine, but it hasn’t opened any connections yet. When it’s first used, it retrieves a connection from a pool of connections maintained by the Engine, and holds onto it until we commit all changes and/or close the session object.

__Step 7: Adding and Updating Objects___
To persist our Employee objects, we add() them to our Session:

```python
akeem = Employee(first_name="Akeem", last_name="Joffer", gender="Male")
session.add(akeem)

session.add_all([Employee("Joe", "Smith", "Male"),
                 Employee("Jill", "Williams", "Female"),
                 Employee("John", "Doe", "Male")]
                )
```

At this point, we say that the instance is pending; no SQL has yet been issued and the object is not yet represented by a row in the database. The Session will issue the SQL to persist Ed Jones as soon as is needed, using a process known as a flush. If we query the database for Ed Jones, all pending information will first be flushed, and the query is issued immediately thereafter.

```python
session.commit()
```

`commit()` flushes the remaining changes to the database, and commits the transaction. The connection resources referenced by the session are now returned to the connection pool. Subsequent operations with this session will occur in a new transaction, which will again re-acquire connection resources when first needed.


__Step 8: Querying__

A Query object is created using the query() method on Session. This function takes a variable number of arguments, which can be any combination of classes and class-instrumented descriptors. Below, we indicate a Query which loads `Employee` instances. When evaluated in an iterative context, the list of `Employee` objects present is returned:

```python
myemployees = session.query(Employee).order_by(Employee.id)
for person in myemployees:
    print person.first_name, person.last_name
```