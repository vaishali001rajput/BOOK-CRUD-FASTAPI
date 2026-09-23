from sqlmodel import SQLModel, Field 
from typing import Optional 
class Book(SQLModel, table=True):   
    id: Optional[int] = Field(default=None, primary_key=True)   
    name: str    
    genre: str
    author : str
    stock : int