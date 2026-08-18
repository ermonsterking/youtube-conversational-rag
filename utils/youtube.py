import re


def extract_video_id(url_or_id: str) -> str:
    """
    Extract a YouTube video ID from a URL or return the ID directly.
    """

    url_or_id = url_or_id.strip()

    # Already a video ID
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id

    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:

        match = re.search(pattern, url_or_id)

        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL or video ID.")