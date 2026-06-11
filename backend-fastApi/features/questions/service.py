from uuid import UUID

from sqlalchemy.orm import Session

from models.question import Question
from models.topic import Topic


class QuestionService:

    def create_question(
        self,
        db: Session,
        topic_id: UUID,
        title: str,
        answer: str,
        difficulty,
    ):
        topic = db.get(
            Topic,
            topic_id,
        )

        if not topic:
            raise ValueError(
                "Topic not found",
            )

        question = Question(
            topic_id=topic_id,
            title=title,
            answer=answer,
            difficulty=difficulty,
        )

        db.add(question)

        db.commit()

        db.refresh(question)

        return question

    def get_question(
        self,
        db: Session,
        question_id: UUID,
    ):
        return db.get(
            Question,
            question_id,
        )

    def get_topic_questions(
        self,
        db: Session,
        topic_id: UUID,
    ):
        return (
            db.query(Question)
            .filter(
                Question.topic_id == topic_id,
            )
            .order_by(
                Question.created_at.desc(),
            )
            .all()
        )

    def update_question(
        self,
        db: Session,
        question_id: UUID,
        title: str,
        answer: str,
        difficulty,
    ):
        question = db.get(
            Question,
            question_id,
        )

        if not question:
            raise ValueError(
                "Question not found",
            )

        question.title = title
        question.answer = answer
        question.difficulty = difficulty

        db.commit()

        db.refresh(question)

        return question

    def delete_question(
        self,
        db: Session,
        question_id: UUID,
    ):
        question = db.get(
            Question,
            question_id,
        )

        if not question:
            raise ValueError(
                "Question not found",
            )

        db.delete(question)

        db.commit()