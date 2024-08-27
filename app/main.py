# Import necessary modules from FastAPI, SQLAlchemy, and datetime
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app import crud, schemas, models  # Import CRUD operations, schemas, and models
from app.database import engine, Base  # Import database engine and base class
from app.auth import get_db, authenticate_user, create_access_token, get_current_user
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES  # Import access token expiration time

# Create an instance of FastAPI
app = FastAPI()

# Create database tables
# This initializes the database schema by creating tables based on the models
Base.metadata.create_all(bind=engine)

# OAuth2 scheme for getting the JWT token
# This is used to specify the URL where the token can be obtained
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Endpoint to create a new user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.
    
    - **user**: The user data provided in the request body.
    - **db**: The database session dependency.
    """
    return crud.create_user(db=db, user=user)

# Endpoint to log in and obtain a JWT token
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return an access token.
    
    - **form_data**: The form data containing username and password.
    - **db**: The database session dependency.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint to get the current user's information
@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.
    
    - **current_user**: The current user obtained from the JWT token.
    """
    return current_user

# Endpoint to create a new product
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Create a new product in the database.
    
    - **product**: The product data provided in the request body.
    - **db**: The database session dependency.
    - **current_user**: The currently authenticated user.
    """
    return crud.create_product(db=db, product=product)

# Endpoint to get a product by its ID
@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Get a product by its ID. Only accessible by the owner of the product.
    
    - **product_id**: The ID of the product to retrieve.
    - **db**: The database session dependency.
    - **current_user**: The currently authenticated user.
    """
    print(f"Current User ID: {current_user.id}")  # Debug statement to print current user ID
    db_product = crud.get_product(db, product_id=product_id, user_id=current_user.id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Endpoint to create a new sale
@app.post("/sales/", response_model=schemas.Sales)
def create_sale(sale: schemas.SalesCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Create a new sale in the database.
    
    - **sale**: The sale data provided in the request body.
    - **db**: The database session dependency.
    - **current_user**: The currently authenticated user.
    """
    return crud.create_sale(db=db, sale=sale)

# Endpoint to get a sale by its ID
@app.get("/sales/{sale_id}", response_model=schemas.Sales)
def read_sale(sale_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Get a sale by its ID.
    
    - **sale_id**: The ID of the sale to retrieve.
    - **db**: The database session dependency.
    - **current_user**: The currently authenticated user.
    """
    db_sale = crud.get_sale(db, sale_id=sale_id)
    print("db_sale saved")  # Debug statement to indicate that the sale was fetched
    if db_sale is None:
        print("ïn the if statement")  # Debug statement if sale is not found
        raise HTTPException(status_code=404, detail="Sale not found")
    print("the end of the funtion")  # Debug statement to indicate function completion
    return db_sale
