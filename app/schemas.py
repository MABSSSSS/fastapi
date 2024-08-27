from pydantic import BaseModel

# Define a schema for the token response
class Token(BaseModel):
    """
    Represents the token response model.
    
    - **access_token**: The JWT token string.
    - **token_type**: The type of the token (e.g., "bearer").
    """
    access_token: str
    token_type: str

# Define a schema for creating a new user
class UserCreate(BaseModel):
    """
    Represents the model for creating a new user.
    
    - **name**: Username for the new user.
    - **password**: Password for the new user.
    """
    name: str
    password: str

# Define a schema for creating a new product
class ProductCreate(BaseModel):
    """
    Represents the model for creating a new product.
    
    - **name**: Name of the product.
    - **price**: Price of the product.
    - **user_id**: Foreign key referencing the user who owns the product.
    """
    name: str
    price: float
    user_id: int

# Define a schema for creating a new sale
class SalesCreate(BaseModel):
    """
    Represents the model for creating a new sale.
    
    - **product_id**: Foreign key referencing the product being sold.
    - **user_id**: Foreign key referencing the user making the sale.
    """
    product_id: int
    user_id: int

# Define a schema for the user model response
class User(BaseModel):
    """
    Represents the user model response.
    
    - **id**: The unique identifier of the user.
    - **name**: The username of the user.
    """
    id: int
    name: str

    class Config:
        """
        Configuration to allow creating models from attributes
        """
        from_attributes = True

# Define a schema for the product model response
class Product(BaseModel):
    """
    Represents the product model response.
    
    - **id**: The unique identifier of the product.
    - **name**: The name of the product.
    - **price**: The price of the product.
    - **user_id**: The user ID of the owner of the product.
    """
    id: int
    name: str
    price: float
    user_id: int

    class Config:
        """
        Configuration to allow creating models from attributes
        """
        from_attributes = True

# Define a schema for the sales model response
class Sales(BaseModel):
    """
    Represents the sales model response.
    
    - **id**: The unique identifier of the sale.
    - **product_id**: The ID of the product sold.
    - **product_name**: The name of the product sold.
    - **user_id**: The ID of the user who made the sale.
    - **user_name**: The name of the user who made the sale.
    """
    id: int
    product_id: int
    product_name: str
    user_id: int
    user_name: str

    class Config:
        """
        Configuration to allow creating models from attributes
        """
        from_attributes = True
