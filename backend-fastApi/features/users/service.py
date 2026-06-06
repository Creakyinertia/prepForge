from sqlalchemy.orm import Session
from models.user import User

class UserService:
    def get_by_email(
        self,
        email:str,
        db:Session
    ):
    return (
        db.query(User)
        .filter(User.email==email)
        .first()
    )