import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_DIR))

import json
from pathlib import Path

from slugify import slugify
import models
from core.database import SessionLocal
from models.roadmap import Roadmap
from models.roadmap_section import (
    RoadmapSection,
)
from models.section_topic import (
    SectionTopic,
)
from models.topic import Topic

DATA_FILE = Path(__file__).parent.parent / "data" / "react-roadmap.json"


def seed():
    db = SessionLocal()

    try:
        with open(
            DATA_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        existing_roadmap = (
            db.query(Roadmap).filter(Roadmap.title == data["title"]).first()
        )

        if existing_roadmap:
            print("Roadmap already exists.")
            return

        roadmap = Roadmap(
            title=data["title"],
            description=data["description"],
            is_published=True,
        )

        db.add(roadmap)
        db.flush()

        for section_index, section_data in enumerate(data["sections"]):
            section = RoadmapSection(
                roadmap_id=roadmap.id,
                title=section_data["title"],
                order_index=section_index,
            )

            db.add(section)
            db.flush()

            for topic_index, topic_title in enumerate(section_data["topics"]):
                slug = slugify(topic_title)

                topic = db.query(Topic).filter(Topic.slug == slug).first()

                if not topic:
                    topic = Topic(
                        title=topic_title,
                        slug=slug,
                    )

                    db.add(topic)
                    db.flush()

                section_topic = SectionTopic(
                    section_id=section.id,
                    topic_id=topic.id,
                    order_index=topic_index,
                )

                db.add(section_topic)

        db.commit()

        print("React roadmap seeded successfully.")

    except Exception as exc:
        db.rollback()

        raise exc

    finally:
        db.close()


if __name__ == "__main__":
    seed()
