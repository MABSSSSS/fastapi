# Import necessary modules from SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

# Define the User model
class User(Base):
    """
    Represents a user in the database.
    
    - **id**: Primary key of the user.
    - **name**: Unique username of the user.
    - **password**: Password hash of the user.
    - **products**: Relationship to the Product model (one-to-many).
    - **sales**: Relationship to the Sale model (one-to-many).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship to Product
    products = relationship("Product", back_populates="owner")

    # Relationship to Sale
    sales = relationship("Sale", back_populates="user")

# Define the Product model
class Product(Base):
    """
    Represents a product in the database.
    
    - **id**: Primary key of the product.
    - **name**: Name of the product.
    - **price**: Price of the product.
    - **user_id**: Foreign key referencing the User model.
    - **owner**: Relationship to the User model (many-to-one).
    - **sales**: Relationship to the Sale model (one-to-many).
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to User
    owner = relationship("User", back_populates="products")

    # Relationship to Sale
    sales = relationship("Sale", back_populates="product")

# Define the Sale model
class Sale(Base):
    """
    Represents a sale in the database.
    
    - **id**: Primary key of the sale.
    - **product_id**: Foreign key referencing the Product model.
    - **user_id**: Foreign key referencing the User model.
    - **product**: Relationship to the Product model (many-to-one).
    - **user**: Relationship to the User model (many-to-one).
    """
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships to Product and User
    product = relationship("Product", back_populates="sales")
    user = relationship("User", back_populates="sales")
