from uuid import UUID
from sqlalchemy.orm import Session
from models.note import Note
from models.topic import Topic

class NoteService:

    def upsert_note(
        self,
        db: Session,
        user_id: UUID,
        topic_id: UUID,
        content: str,
    ):
        topic = db.get(
            Topic,
            topic_id,
        )

        if not topic:
            raise ValueError(
                "Topic not found",
            )

        note = (
            db.query(Note)
            .filter(
                Note.user_id == user_id,
                Note.topic_id == topic_id,
            )
            .first()
        )

        if not note:
            note = Note(
                user_id=user_id,
                topic_id=topic_id,
                content=content,
            )

            db.add(note)

        else:
            note.content = content

        db.commit()
        db.refresh(note)

        return note

    def get_note(
        self,
        db: Session,
        user_id: UUID,
        topic_id: UUID,
    ):
        return (
            db.query(Note)
            .filter(
                Note.user_id == user_id,
                Note.topic_id == topic_id,
            )
            .first()
        )