from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID
from datetime import datetime, timedelta, timezone
from core.security import hash_password, generate_refresh_token, hash_refresh_token, create_access_token, verify_password
from models.user import User
from core.config import settings
from models.refresh_token import RefreshToken
from core.exceptions import AuthenticationError

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
            raise AuthenticationError()
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
        return raw_token
    
    def refresh_access_token(
        self,
        db:Session,
        refresh_token:str
    ):
        token_hash = hash_refresh_token(
            refresh_token
        )

        session = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash
            )
            .first()
        )

        if not session:
            raise InvalidRefreshTokenError()

        if session.revoked_at:
            raise InvalidRefreshTokenError()

        if session.expires_at < datetime.now(timezone.utc):
            raise InvalidRefreshTokenError()

        user = db.get(
            User,
            session.user_id,
        )

        if not user:
            raise InvalidRefreshTokenError()

        session.revoked_at = datetime.now(
            timezone.utc
        )

        new_refresh_token = (
            self.create_refresh_session(
                db,
                user.id,
            )
        )

        access_token = create_access_token(
            str(user.id)
        )

        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    def login(
        self,
        db:Session,
        email: str,
        password: str
    ):
        user = db.query(User).filter(User.email==email).first()
        if not user:
            raise AuthenticationError()
        if not verify_password(
            password,
            user.hashed_password
        ):
            raise AuthenticationError()

        access_token = create_access_token(
            str(user.id)
        )

        refresh_token = self.create_refresh_session(
            db,
            user.id
        )
        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def logout(
        self,
        db: Session,
        refresh_token: str,
    ):
        token_hash = hash_refresh_token(
            refresh_token
        )

        session = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash
            )
            .first()
        )

        if session:
            session.revoked_at = datetime.now(
                timezone.utc
            )

            db.commit()

    def logout_all(
        self,
        db: Session,
        user_id: UUID,
    ):
        (
            db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .update(
                {
                    RefreshToken.revoked_at:
                    datetime.now(timezone.utc)
                }
            )
        )
    
        db.commit()