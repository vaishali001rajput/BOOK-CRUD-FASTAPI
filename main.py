from fastapi import FastAPI , Depends , HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel , select
from sqlalchemy.exc import OperationalError 
from database import engine , Session ,get_session
from models import Book 
app = FastAPI() 
@app.on_event("startup") 
def on_startup():    
    try:        
        SQLModel.metadata.create_all(engine)    
        print("Database Connected Successfully!") 
    except OperationalError as e:       
        print("Database Connection Failed:", e)
        
        
@app.get("/")
def home():
    return{"message" : "welcome to FastAPI"}

@app.post("/student") 
def add_student(book:Book , session: Session = Depends(get_session)):  
    session.add(book)  
    session.commit()   
    session.refresh(book) 
    return book


  
# CREATE - ADD BOOK
@app.post("/book")
def add_book(
    book: Book,  
    session: Session = Depends(get_session)
):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# READ ONE - GET BOOK BY ID
@app.get("/book/{book_id}")
def get_book(
    book_id: int,
    session: Session = Depends(get_session)   
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book nahi mili"  # Fixed: 'detail' instead of 'details'
        )
    return book  # Fixed: Moved outside 'if' block


# UPDATE - Update Book
@app.put("/book/{book_id}")
def update_book(
    book_id: int,
    updated: Book,  # Fixed: Capital 'B'
    session: Session = Depends(get_session)
):
    book = session.get(Book, book_id)  # Fixed: Capital 'B'
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book nahi mili"
        )
        
    # Fixed: Moved outside 'if' block
    book.name = updated.name
    book.genre = updated.genre
    book.author = updated.author
    book.stock = updated.stock
    
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# DELETE - Delete Book
# Fixed: Moved outside update_book function
@app.delete("/book/{book_id}")
def delete_book(
    book_id: int,
    session: Session = Depends(get_session)  # Fixed: Capital 'S'
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book nahi mili"
        )
        
    # Fixed: Moved outside 'if' block
    session.delete(book)
    session.commit()
    return {"message": "Book successfully delete ho gayi"}
  
   
    


