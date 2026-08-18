from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_id: str):

    api = YouTubeTranscriptApi()

    transcript = api.fetch(
        video_id,
        languages=["en", "hi"]
    )

    return transcript