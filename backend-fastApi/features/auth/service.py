from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timedelta, timezone
from core.security import hash_password, generate_refresh_token, hash_refresh_token, create_access_token, verify_password
from models.user import User
from core.config import settings
from models.refresh_token import RefreshToken

class AuthService:
    def register(
        self,
        db:Session,
        email:str,
        username:str,
        password:str
    ):
        existing_user = (
            db.query(User)
            .filter(
                or_(
                    User.email == email,
                    User.username == username,
                )
            )
            .first()
        )
        if existing_user:
            raise ValueError("User already exists")
        user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def create_refresh_session(
        self,
        db:Session,
        user_id: UUID
    )->str:
        raw_token = generate_refresh_token()
        token_hash = hash_refresh_token(
            raw_token
        )
        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        )
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return raw_token

    def login(
        self,
        db:Session,
        email: str,
        password: str
    ):
        user = db.query(User).filter(User.email==email).first()
        if not user:
            raise ValueError("Invalid credentials")
        if not verify_password(
            password,
            user.hashed_password
        ):
            raise ValueError("Invalid credentials")

        access_token = create_access_token(
            str(user.id)
        )

        refresh_token = self.create_refresh_session(
            db,
            user.id
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "type": "bearer"
        }