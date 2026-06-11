from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import MagicMock

from features.home import router
from features.home.schema import HomeResponse
from features.home.service import HomeService
from models.enums import TopicProgressStatus


def test_home_response_schema_accepts_expected_payload():
    payload = HomeResponse(
        continue_learning=[
            {
                "topic_id": uuid4(),
                "title": "Trees",
                "slug": "trees",
                "progress_status": "IN_PROGRESS",
            }
        ],
        due_revisions=3,
        recent_bookmarks=[
            {
                "id": uuid4(),
                "topic_id": uuid4(),
                "topic_title": "Graphs",
                "topic_slug": "graphs",
                "topic_description": "Traversal patterns",
            }
        ],
    )

    assert payload.due_revisions == 3
    assert payload.continue_learning[0].progress_status == "IN_PROGRESS"


def test_get_home_data_returns_expected_payload():
    service = HomeService()
    db = MagicMock()
    user_id = uuid4()

    continue_learning_query = MagicMock()
    continue_learning_query.join.return_value = continue_learning_query
    continue_learning_query.filter.return_value = continue_learning_query
    continue_learning_query.order_by.return_value = continue_learning_query
    continue_learning_query.limit.return_value = continue_learning_query
    continue_learning_query.all.return_value = [
        (
            SimpleNamespace(
                status=TopicProgressStatus.IN_PROGRESS,
            ),
            SimpleNamespace(
                id=uuid4(),
                title="Dynamic Programming",
                slug="dynamic-programming",
            ),
        )
    ]

    due_revisions_query = MagicMock()
    due_revisions_query.select_from.return_value = due_revisions_query
    due_revisions_query.filter.return_value = due_revisions_query
    due_revisions_query.scalar.return_value = 4

    bookmark_topic = SimpleNamespace(
        title="Graphs",
        slug="graphs",
        description="Graph basics",
    )
    bookmarks_query = MagicMock()
    bookmarks_query.filter.return_value = bookmarks_query
    bookmarks_query.order_by.return_value = bookmarks_query
    bookmarks_query.limit.return_value = bookmarks_query
    bookmarks_query.all.return_value = [
        SimpleNamespace(
            id=uuid4(),
            topic_id=uuid4(),
            topic=bookmark_topic,
        )
    ]

    db.query.side_effect = [
        continue_learning_query,
        due_revisions_query,
        bookmarks_query,
    ]

    result = service.get_home_data(
        db,
        user_id,
    )

    assert result == {
        "continue_learning": [
            {
                "topic_id": continue_learning_query.all.return_value[0][1].id,
                "title": "Dynamic Programming",
                "slug": "dynamic-programming",
                "progress_status": TopicProgressStatus.IN_PROGRESS,
            }
        ],
        "due_revisions": 4,
        "recent_bookmarks": [
            {
                "id": bookmarks_query.all.return_value[0].id,
                "topic_id": bookmarks_query.all.return_value[0].topic_id,
                "topic_title": "Graphs",
                "topic_slug": "graphs",
                "topic_description": "Graph basics",
            }
        ],
    }


def test_get_home_router_returns_service_payload(monkeypatch):
    expected = {
        "continue_learning": [],
        "due_revisions": 0,
        "recent_bookmarks": [],
    }

    monkeypatch.setattr(
        router.home_service,
        "get_home_data",
        lambda db, user_id: expected,
    )

    result = router.get_home(
        current_user=SimpleNamespace(id=uuid4()),
        db=MagicMock(),
    )

    assert result == expected
