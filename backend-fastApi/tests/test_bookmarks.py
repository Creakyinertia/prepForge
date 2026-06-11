from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from core.exceptions import NotFoundError
from features.bookmarks import router
from features.bookmarks.schema import BookmarkResponse
from features.bookmarks.service import BookmarkService


def test_bookmark_response_schema_accepts_expected_payload():
    payload = BookmarkResponse(
        id=uuid4(),
        topic_id=uuid4(),
        topic_title="Arrays",
        topic_slug="arrays",
        topic_description="Intro arrays",
    )

    assert payload.topic_slug == "arrays"


def test_create_bookmark_raises_for_missing_topic():
    service = BookmarkService()
    db = MagicMock()
    db.get.return_value = None

    with pytest.raises(NotFoundError, match="Topic not found"):
        service.create_bookmark(
            db,
            uuid4(),
            uuid4(),
        )


def test_create_bookmark_returns_existing_bookmark_without_writes():
    service = BookmarkService()
    db = MagicMock()
    user_id = uuid4()
    topic_id = uuid4()
    topic = SimpleNamespace(
        title="Trees",
        slug="trees",
        description="Binary trees",
    )
    existing_bookmark = SimpleNamespace(
        id=uuid4(),
        topic_id=topic_id,
        topic=topic,
    )

    bookmark_query = MagicMock()
    bookmark_query.filter.return_value = bookmark_query
    bookmark_query.first.return_value = existing_bookmark

    db.get.return_value = topic
    db.query.return_value = bookmark_query

    result = service.create_bookmark(
        db,
        user_id,
        topic_id,
    )

    assert result == {
        "id": existing_bookmark.id,
        "topic_id": topic_id,
        "topic_title": "Trees",
        "topic_slug": "trees",
        "topic_description": "Binary trees",
    }
    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_create_bookmark_persists_new_bookmark():
    service = BookmarkService()
    db = MagicMock()
    user_id = uuid4()
    topic_id = uuid4()
    topic = SimpleNamespace(
        title="Queues",
        slug="queues",
        description="FIFO structures",
    )

    bookmark_query = MagicMock()
    bookmark_query.filter.return_value = bookmark_query
    bookmark_query.first.return_value = None

    db.get.return_value = topic
    db.query.return_value = bookmark_query

    class FakeBookmarkedTopic:
        user_id = object()
        topic_id = object()

        def __init__(self, user_id, topic_id):
            self.user_id = user_id
            self.topic_id = topic_id

    def assign_bookmark_id(bookmark):
        bookmark.id = uuid4()
        bookmark.topic = topic

    db.add.side_effect = assign_bookmark_id

    original_bookmarked_topic = service.create_bookmark.__globals__["BookmarkedTopic"]
    service.create_bookmark.__globals__["BookmarkedTopic"] = FakeBookmarkedTopic

    try:
        result = service.create_bookmark(
            db,
            user_id,
            topic_id,
        )
    finally:
        service.create_bookmark.__globals__["BookmarkedTopic"] = original_bookmarked_topic

    assert result["topic_id"] == topic_id
    assert result["topic_title"] == "Queues"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_remove_bookmark_deletes_existing_bookmark():
    service = BookmarkService()
    db = MagicMock()
    bookmark = SimpleNamespace(id=uuid4())

    bookmark_query = MagicMock()
    bookmark_query.filter.return_value = bookmark_query
    bookmark_query.first.return_value = bookmark
    db.query.return_value = bookmark_query

    service.remove_bookmark(
        db,
        uuid4(),
        uuid4(),
    )

    db.delete.assert_called_once_with(bookmark)
    db.commit.assert_called_once()


def test_remove_bookmark_raises_for_missing_bookmark():
    service = BookmarkService()
    db = MagicMock()

    bookmark_query = MagicMock()
    bookmark_query.filter.return_value = bookmark_query
    bookmark_query.first.return_value = None
    db.query.return_value = bookmark_query

    with pytest.raises(NotFoundError, match="Bookmark not found"):
        service.remove_bookmark(
            db,
            uuid4(),
            uuid4(),
        )


def test_get_bookmarks_returns_mapped_payload():
    service = BookmarkService()
    db = MagicMock()
    bookmark = SimpleNamespace(
        id=uuid4(),
        topic_id=uuid4(),
        topic=SimpleNamespace(
            title="Heap",
            slug="heap",
            description=None,
        ),
    )

    bookmark_query = MagicMock()
    bookmark_query.filter.return_value = bookmark_query
    bookmark_query.order_by.return_value = bookmark_query
    bookmark_query.all.return_value = [bookmark]
    db.query.return_value = bookmark_query

    result = service.get_bookmarks(
        db,
        uuid4(),
    )

    assert result == [
        {
            "id": bookmark.id,
            "topic_id": bookmark.topic_id,
            "topic_title": "Heap",
            "topic_slug": "heap",
            "topic_description": None,
        }
    ]


def test_create_bookmark_router_returns_service_payload(monkeypatch):
    expected = {
        "id": uuid4(),
        "topic_id": uuid4(),
        "topic_title": "Graphs",
        "topic_slug": "graphs",
        "topic_description": "Graph traversal",
    }

    monkeypatch.setattr(
        router.bookmark_service,
        "create_bookmark",
        lambda db, user_id, topic_id: expected,
    )

    result = router.create_bookmark(
        expected["topic_id"],
        current_user=SimpleNamespace(id=uuid4()),
        db=MagicMock(),
    )

    assert result == expected


def test_create_bookmark_router_translates_not_found(monkeypatch):
    def raise_not_found(db, user_id, topic_id):
        raise NotFoundError("Topic not found")

    monkeypatch.setattr(
        router.bookmark_service,
        "create_bookmark",
        raise_not_found,
    )

    with pytest.raises(HTTPException) as exc_info:
        router.create_bookmark(
            uuid4(),
            current_user=SimpleNamespace(id=uuid4()),
            db=MagicMock(),
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Topic not found"


def test_remove_bookmark_router_returns_confirmation(monkeypatch):
    removed = {}

    def fake_remove(db, user_id, topic_id):
        removed["topic_id"] = topic_id

    monkeypatch.setattr(
        router.bookmark_service,
        "remove_bookmark",
        fake_remove,
    )

    topic_id = uuid4()
    result = router.remove_bookmark(
        topic_id,
        current_user=SimpleNamespace(id=uuid4()),
        db=MagicMock(),
    )

    assert removed["topic_id"] == topic_id
    assert result == {"message": "Bookmark removed"}


def test_remove_bookmark_router_translates_not_found(monkeypatch):
    def raise_not_found(db, user_id, topic_id):
        raise NotFoundError("Bookmark not found")

    monkeypatch.setattr(
        router.bookmark_service,
        "remove_bookmark",
        raise_not_found,
    )

    with pytest.raises(HTTPException) as exc_info:
        router.remove_bookmark(
            uuid4(),
            current_user=SimpleNamespace(id=uuid4()),
            db=MagicMock(),
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Bookmark not found"


def test_get_bookmarks_router_returns_service_payload(monkeypatch):
    expected = [
        {
            "id": uuid4(),
            "topic_id": uuid4(),
            "topic_title": "Sorting",
            "topic_slug": "sorting",
            "topic_description": "Sorting basics",
        }
    ]

    monkeypatch.setattr(
        router.bookmark_service,
        "get_bookmarks",
        lambda db, user_id: expected,
    )

    result = router.get_bookmarks(
        current_user=SimpleNamespace(id=uuid4()),
        db=MagicMock(),
    )

    assert result == expected
