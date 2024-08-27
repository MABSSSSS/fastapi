# Import necessary libraries
from datetime import datetime, timedelta  # For handling date and time operations
from jose import JWTError, jwt  # For creating and decoding JWT tokens
from passlib.context import CryptContext  # For hashing and verifying passwords
from fastapi import Depends, HTTPException, status  # For handling HTTP exceptions and request dependencies
from sqlalchemy.orm import Session  # For SQLAlchemy ORM session management
from fastapi.security import OAuth2PasswordBearer  # For handling OAuth2 Bearer tokens
from app import models, crud  # Import application-specific models and CRUD operations
from app.database import SessionLocal  # Import the database session factory

# Secret key used for encoding and decoding JWT tokens
SECRET_KEY = "a_secure_secret_key"
# Algorithm used for encoding JWT tokens
ALGORITHM = "HS256"
# Token expiration time (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create a password hashing context using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize OAuth2PasswordBearer instance with the URL for obtaining tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency function to get a SQLAlchemy database session
def get_db():
    """
    Provides a SQLAlchemy database session.
    
    This function creates a new database session, yields it to the caller, 
    and ensures that the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility function to hash passwords
def get_password_hash(password: str) -> str:
    """
    Hashes a plain password using bcrypt.
    
    Args:
        password (str): The plain text password to hash.
        
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

# Utility function to verify if a plain password matches the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    
    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.
        
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Utility function to create a JWT access token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token with an expiration time.
    
    Args:
        data (dict): The data to include in the token payload.
        expires_delta (timedelta | None): The expiration time of the token.
        
    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Utility function to authenticate a user based on username and password
def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticates a user by checking their username and password.
    
    Args:
        db (Session): The database session.
        username (str): The username of the user.
        password (str): The password of the user.
        
    Returns:
        User | False: The user object if authentication is successful, False otherwise.
    """
    user = db.query(models.User).filter(models.User.name == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# Utility function to get the current authenticated user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """
    Retrieves the current user based on the JWT token.
    
    Args:
        token (str): The JWT token from the request.
        db (Session): The database session.
        
    Returns:
        User: The authenticated user object.
        
    Raises:
        HTTPException: If the token is invalid or the user cannot be found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.name == username).first()
    if user is None:
        raise credentials_exception
    return user
