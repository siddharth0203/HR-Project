
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    email: str
    phone_number: int 
    current_status: str
    resume_link: str
   