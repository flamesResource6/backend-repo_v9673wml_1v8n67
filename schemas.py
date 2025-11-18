"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List

# Example schemas (retain for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Academy schemas

class Course(BaseModel):
    """Courses offered by the academy"""
    title: str = Field(..., min_length=2)
    summary: str = Field(..., min_length=10)
    duration_weeks: int = Field(..., ge=1, le=104)
    level: str = Field(..., description="Beginner, Intermediate, Advanced")
    tags: List[str] = Field(default_factory=list)
    thumbnail: Optional[HttpUrl] = None

class Instructor(BaseModel):
    """Instructors teaching at the academy"""
    name: str
    title: str
    bio: str
    avatar: Optional[HttpUrl] = None
    specialties: List[str] = Field(default_factory=list)

class Enrollment(BaseModel):
    """Enrollment application submitted by a learner"""
    name: str = Field(..., min_length=2)
    email: EmailStr
    course_title: str
    message: Optional[str] = Field(None, max_length=1000)
