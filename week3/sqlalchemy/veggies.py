from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# NOTE - Make sure venv is active - windows: . venv/scripts/activate & docker containers are up and running.

# This creates a database connection. Under the hood, this SQLAlchemy engine uses psycopg2 to establish the connection:
# Connect to Postgres database
engine = create_engine('postgresql://postgres@localhost:5432/week3')
# sessionmaker gives us the ability to interact with the database via the engine:
Session = sessionmaker(bind=engine)
# Create the Base class using an SQLAlchemy utility called declarative_base(). Each model (Python class) that we want SQLAlchemy to map to a database table must inherit this Base class.
Base = declarative_base()

# Defines a class named Veggie in Python which we will map to the veggies table in SQL:
class Veggie(Base):
    # __tablename__ specifies the name of the SQL table this class should map to
    __tablename__ = "veggies"

    # SQLAlchemy-provided Column class to define the column mappings:

    # set autoincrement to use the SERIAL data type (The special parameter autoincrement=True will assign to it the SERIAL data type in Postgres)
    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String, nullable=False)
    name = Column(String, nullable=False)

    # formatted_name method references the self keyword to get the values of name and color for a given instance of a Veggie object
    def formatted_name(self):
        return self.color.capitalize() + " " + self.name.capitalize()



# Recreate all tables each time script is run
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Defines the initial data with which we will seed the table, using a list of dictionaries (Key represents the column while the value represents the value for the column):
seed_data = [
    {'name': 'carrot', 'color': 'orange'},
    {'name': 'onion', 'color': 'yellow'},
    {'name': 'zucchini', 'color': 'green'},
    {'name': 'squash', 'color': 'yellow'},
    {'name': 'pepper', 'color': 'red'},
    {'name': 'onion', 'color': 'red'}
]

# Turn the seed data into a list of Veggie objects
veggie_objects = []
for item in seed_data:
    v = Veggie(name=item["name"], color=item["color"])
    veggie_objects.append(v)

# To insert the objects as SQL records, we have to begin a new session.

# Create a session, insert new records, and commit the session
session = Session()
# pass our veggie_objects to the bulk_save_objects() method:
session.bulk_save_objects(veggie_objects)
# To get SQLAlchemy to generate the SQL and perform the inserts, we call the session's commit() method:
session.commit()


# Create a new session for performing queries (Since we committed our previous session to insert the veggie records, we need to open a new session to continue on.)
session = Session()

# Run a SELECT * query on the veggies table (Retrieve all the records from the table created by the Veggie model and store them in the variable veggies as a list of objects.)
veggies = session.query(Veggie).all()

for v in veggies:
    print(v.color, v.name)

# SELECT * FROM veggies ORDER BY name, color
veggies = session.query(Veggie).order_by(
    Veggie.name, Veggie.color).all()

for i, v in enumerate(veggies):
    print(str(i+1) + ". " + v.formatted_name())
