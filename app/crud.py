# Import necessary modules
from sqlalchemy.orm import Session  # For SQLAlchemy ORM session management
from app import models, schemas  # Import application-specific models and schemas
from app.auth import get_password_hash  # Import utility for hashing passwords

# Function to create a new user in the database
def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user and saves it to the database.
    
    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The user data to create.
        
    Returns:
        models.User: The created user object.
    """
    # Hash the provided password
    hashed_password = get_password_hash(user.password)
    # Create a new User instance with the hashed password
    db_user = models.User(name=user.name, password=hashed_password)
    # Add the new user to the session
    db.add(db_user)
    # Commit the transaction to save the user to the database
    db.commit()
    # Refresh the user instance to get the updated state from the database
    db.refresh(db_user)
    return db_user

# Function to retrieve a user by ID
def get_user(db: Session, user_id: int):
    """
    Retrieves a user from the database by its ID.
    
    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.
        
    Returns:
        models.User | None: The user object if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

# Function to create a new product in the database
def create_product(db: Session, product: schemas.ProductCreate):
    """
    Creates a new product and saves it to the database.
    
    Args:
        db (Session): The database session.
        product (schemas.ProductCreate): The product data to create.
        
    Returns:
        models.Product: The created product object.
    """
    # Create a new Product instance
    db_product = models.Product(name=product.name, price=product.price, user_id=product.user_id)
    # Add the new product to the session
    db.add(db_product)
    # Commit the transaction to save the product to the database
    db.commit()
    # Refresh the product instance to get the updated state from the database
    db.refresh(db_product)
    return db_product

# Function to retrieve a product by ID and ensure it belongs to a specific user
def get_product(db: Session, product_id: int, user_id: int):
    """
    Retrieves a product from the database by its ID and ensures it belongs to the given user.
    
    Args:
        db (Session): The database session.
        product_id (int): The ID of the product to retrieve.
        user_id (int): The ID of the user who should own the product.
        
    Returns:
        models.Product | None: The product object if found and belongs to the user, otherwise None.
    """
    return db.query(models.Product).filter(models.Product.id == product_id, models.Product.user_id == user_id).first()

# Function to create a new sale in the database
def create_sale(db: Session, sale: schemas.SalesCreate):
    """
    Creates a new sale and saves it to the database. Checks if the related product and user exist.
    
    Args:
        db (Session): The database session.
        sale (schemas.SalesCreate): The sale data to create.
        
    Returns:
        dict: A dictionary containing the sale details including product and user names.
        
    Raises:
        ValueError: If the product or user does not exist.
    """
    # Ensure that the product exists
    product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
    # Ensure that the user exists
    user = db.query(models.User).filter(models.User.id == sale.user_id).first()
    
    if not product:
        raise ValueError("Product not found")
    if not user:
        raise ValueError("User not found")
    
    # Create a new Sale instance
    db_sale = models.Sale(product_id=sale.product_id, user_id=sale.user_id)
    # Add the new sale to the session
    db.add(db_sale)
    # Commit the transaction to save the sale to the database
    db.commit()
    # Refresh the sale instance to get the updated state from the database
    db.refresh(db_sale)
    # Return a dictionary with sale details, including product and user names
    return {
        "id": db_sale.id,
        "product_id": db_sale.product_id,
        "product_name": product.name,
        "user_id": db_sale.user_id,
        "user_name": user.name
    }

# Function to retrieve a sale by ID and include related product and user details
def get_sale(db: Session, sale_id: int):
    """
    Retrieves a sale from the database by its ID and includes related product and user details.
    
    Args:
        db (Session): The database session.
        sale_id (int): The ID of the sale to retrieve.
        
    Returns:
        Sale | None: A tuple containing sale details, product name, and user name if found, otherwise None.
    """
    # Join Sale with Product and User to get additional fields
    sale_query = db.query(
        models.Sale.id,
        models.Sale.product_id,
        models.Sale.user_id,
        models.Product.name.label("product_name"),
        models.User.name.label("user_name")
    ).join(
        models.Product, models.Sale.product_id == models.Product.id
    ).join(
        models.User, models.Sale.user_id == models.User.id
    ).filter(
        models.Sale.id == sale_id
    ).first()
    
    # Print the query result for debugging purposes
    print(f"Query result: {sale_query}")
    
    return sale_query
