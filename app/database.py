# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine  # Used to create a database engine
from sqlalchemy.ext.declarative import declarative_base  # Base class for declarative class definitions
from sqlalchemy.orm import sessionmaker  # Factory to create new Session objects

# Database URL for PostgreSQL
DATABASE_URL = "postgresql://postgres:1234@localhost/fastapi"

# Create a database engine
# The engine is responsible for managing connections to the database and executing SQL statements
engine = create_engine(DATABASE_URL)

# Create a session factory
# SessionLocal is a factory for creating new SQLAlchemy Session objects
# Session objects are used to interact with the database
SessionLocal = sessionmaker(
    autocommit=False,  # Sessions do not automatically commit transactions
    autoflush=False,   # Sessions do not automatically flush changes to the database
    bind=engine        # Bind the session to the created engine
)

# Create a base class for declarative class definitions
# Declarative base is used to define the mapping between Python classes and database tables
Base = declarative_base()
