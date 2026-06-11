from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from core.exceptions import NotFoundError
from features.readiness import router
from features.readiness.schema import (
    RoadmapReadinessResponse,
    TopicReadinessResponse,
)
from features.readiness.service import ReadinessService
from models.enums import (
    QuestionStatus,
    TopicProgressStatus,
)


def test_topic_readiness_response_schema_accepts_service_shape():
    payload = TopicReadinessResponse(
        topic_id=uuid4(),
        topic_title="Arrays",
        topic_completed=True,
        total_questions=10,
        mastered_questions=8,
        due_revisions=1,
        readiness_score=80.0,
    )

    assert payload.topic_title == "Arrays"
    assert payload.readiness_score == 80.0


def test_roadmap_readiness_response_schema_accepts_service_shape():
    payload = RoadmapReadinessResponse(
        roadmap_id=uuid4(),
        roadmap_title="DSA",
        total_topics=12,
        completed_topics=6,
        readiness_score=75.5,
    )

    assert payload.completed_topics == 6
    assert payload.readiness_score == 75.5


def test_calculate_score_handles_full_credit():
    service = ReadinessService()

    score = service.calculate_score(
        topic_completed=True,
        total_questions=10,
        mastered_questions=8,
        due_revisions=0,
    )

    assert score == 90.0


def test_calculate_score_handles_zero_questions():
    service = ReadinessService()

    score = service.calculate_score(
        topic_completed=False,
        total_questions=0,
        mastered_questions=0,
        due_revisions=3,
    )

    assert score == 0


def test_get_topic_readiness_returns_expected_payload():
    service = ReadinessService()
    db = MagicMock()
    user_id = uuid4()
    topic_id = uuid4()
    topic = SimpleNamespace(id=topic_id, title="Graphs")
    progress = SimpleNamespace(
        status=TopicProgressStatus.COMPLETED,
    )

    progress_query = MagicMock()
    progress_query.filter.return_value = progress_query
    progress_query.first.return_value = progress

    total_query = MagicMock()
    total_query.select_from.return_value = total_query
    total_query.filter.return_value = total_query
    total_query.scalar.return_value = 10

    mastered_query = MagicMock()
    mastered_query.select_from.return_value = mastered_query
    mastered_query.join.return_value = mastered_query
    mastered_query.filter.return_value = mastered_query
    mastered_query.scalar.return_value = 7

    revisions_query = MagicMock()
    revisions_query.select_from.return_value = revisions_query
    revisions_query.filter.return_value = revisions_query
    revisions_query.scalar.return_value = 2

    db.get.return_value = topic
    db.query.side_effect = [
        progress_query,
        total_query,
        mastered_query,
        revisions_query,
    ]

    result = service.get_topic_readiness(
        db,
        user_id,
        topic_id,
    )

    assert result == {
        "topic_id": topic_id,
        "topic_title": "Graphs",
        "topic_completed": True,
        "total_questions": 10,
        "mastered_questions": 7,
        "due_revisions": 2,
        "readiness_score": 75.0,
    }


def test_get_topic_readiness_raises_for_missing_topic():
    service = ReadinessService()
    db = MagicMock()
    db.get.return_value = None

    with pytest.raises(NotFoundError, match="Topic not found"):
        service.get_topic_readiness(
            db,
            uuid4(),
            uuid4(),
        )


def test_get_roadmap_readiness_returns_zeroes_for_empty_roadmap():
    service = ReadinessService()
    db = MagicMock()
    roadmap_id = uuid4()
    roadmap = SimpleNamespace(
        id=roadmap_id,
        title="Backend",
    )

    roadmap_topics_query = MagicMock()
    roadmap_topics_query.filter.return_value = roadmap_topics_query
    roadmap_topics_query.all.return_value = []

    db.get.return_value = roadmap
    db.query.return_value = roadmap_topics_query

    result = service.get_roadmap_readiness(
        db,
        uuid4(),
        roadmap_id,
    )

    assert result == {
        "roadmap_id": roadmap_id,
        "roadmap_title": "Backend",
        "total_topics": 0,
        "completed_topics": 0,
        "readiness_score": 0,
    }


def test_get_roadmap_readiness_returns_expected_payload():
    service = ReadinessService()
    db = MagicMock()
    user_id = uuid4()
    roadmap_id = uuid4()
    roadmap = SimpleNamespace(
        id=roadmap_id,
        title="System Design",
    )
    topic_ids = [uuid4(), uuid4()]

    roadmap_topics_query = MagicMock()
    roadmap_topics_query.filter.return_value = roadmap_topics_query
    roadmap_topics_query.all.return_value = [
        SimpleNamespace(topic_id=topic_ids[0]),
        SimpleNamespace(topic_id=topic_ids[1]),
    ]

    completed_topics_query = MagicMock()
    completed_topics_query.filter.return_value = completed_topics_query
    completed_topics_query.count.return_value = 1

    total_questions_query = MagicMock()
    total_questions_query.filter.return_value = total_questions_query
    total_questions_query.count.return_value = 8

    mastered_questions_query = MagicMock()
    mastered_questions_query.join.return_value = mastered_questions_query
    mastered_questions_query.filter.return_value = mastered_questions_query
    mastered_questions_query.count.return_value = 6

    db.get.return_value = roadmap
    db.query.side_effect = [
        roadmap_topics_query,
        completed_topics_query,
        total_questions_query,
        mastered_questions_query,
    ]

    result = service.get_roadmap_readiness(
        db,
        user_id,
        roadmap_id,
    )

    assert result == {
        "roadmap_id": roadmap_id,
        "roadmap_title": "System Design",
        "total_topics": 2,
        "completed_topics": 1,
        "readiness_score": 62.5,
    }


def test_get_roadmap_readiness_raises_for_missing_roadmap():
    service = ReadinessService()
    db = MagicMock()
    db.get.return_value = None

    with pytest.raises(NotFoundError, match="Roadmap not found"):
        service.get_roadmap_readiness(
            db,
            uuid4(),
            uuid4(),
        )


def test_get_all_roadmap_readiness_aggregates_all_roadmaps(monkeypatch):
    service = ReadinessService()
    db = MagicMock()
    user_id = uuid4()
    roadmaps = [
        SimpleNamespace(id=uuid4(), title="A"),
        SimpleNamespace(id=uuid4(), title="B"),
    ]

    roadmap_query = MagicMock()
    roadmap_query.order_by.return_value = roadmap_query
    roadmap_query.all.return_value = roadmaps
    db.query.return_value = roadmap_query

    expected = {
        roadmaps[0].id: {"roadmap_id": roadmaps[0].id, "readiness_score": 10},
        roadmaps[1].id: {"roadmap_id": roadmaps[1].id, "readiness_score": 20},
    }

    monkeypatch.setattr(
        service,
        "get_roadmap_readiness",
        lambda current_db, current_user_id, roadmap_id: expected[roadmap_id],
    )

    result = service.get_all_roadmap_readiness(
        db,
        user_id,
    )

    assert result == [
        expected[roadmaps[0].id],
        expected[roadmaps[1].id],
    ]


def test_get_topic_readiness_router_returns_service_payload(monkeypatch):
    topic_id = uuid4()
    user_id = uuid4()
    expected = {
        "topic_id": topic_id,
        "topic_title": "Stacks",
        "topic_completed": False,
        "total_questions": 3,
        "mastered_questions": 1,
        "due_revisions": 0,
        "readiness_score": 26.67,
    }

    monkeypatch.setattr(
        router.readiness_service,
        "get_topic_readiness",
        lambda db, current_user_id, current_topic_id: expected,
    )

    result = router.get_topic_readiness(
        topic_id,
        current_user=SimpleNamespace(id=user_id),
        db=MagicMock(),
    )

    assert result == expected


def test_get_topic_readiness_router_translates_not_found(monkeypatch):
    def raise_not_found(db, current_user_id, current_topic_id):
        raise NotFoundError("Topic not found")

    monkeypatch.setattr(
        router.readiness_service,
        "get_topic_readiness",
        raise_not_found,
    )

    with pytest.raises(HTTPException) as exc_info:
        router.get_topic_readiness(
            uuid4(),
            current_user=SimpleNamespace(id=uuid4()),
            db=MagicMock(),
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Topic not found"


def test_get_roadmap_readiness_router_translates_not_found(monkeypatch):
    def raise_not_found(db, current_user_id, current_roadmap_id):
        raise NotFoundError("Roadmap not found")

    monkeypatch.setattr(
        router.readiness_service,
        "get_roadmap_readiness",
        raise_not_found,
    )

    with pytest.raises(HTTPException) as exc_info:
        router.get_roadmap_readiness(
            uuid4(),
            current_user=SimpleNamespace(id=uuid4()),
            db=MagicMock(),
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Roadmap not found"


def test_get_all_roadmap_readiness_router_returns_service_payload(monkeypatch):
    expected = [
        {
            "roadmap_id": uuid4(),
            "roadmap_title": "Algorithms",
            "total_topics": 5,
            "completed_topics": 2,
            "readiness_score": 40.0,
        }
    ]

    monkeypatch.setattr(
        router.readiness_service,
        "get_all_roadmap_readiness",
        lambda db, current_user_id: expected,
    )

    result = router.get_all_roadmap_readiness(
        current_user=SimpleNamespace(id=uuid4()),
        db=MagicMock(),
    )

    assert result == expected


def test_enums_still_expose_expected_status_values():
    assert QuestionStatus.MASTERED.value == "MASTERED"
    assert TopicProgressStatus.COMPLETED.value == "COMPLETED"
