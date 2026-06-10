import re

def generate_slug(title: str) -> str:
    slug = title.lower()

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        slug,
    )

    return slug.strip("-")