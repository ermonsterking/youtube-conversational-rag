from utils.youtube_transcript import get_transcript


video_id = "kFHSf2oS5l0"

transcript = get_transcript(video_id)

print("Transcript retrieved successfully")
print("Number of snippets:", len(transcript))

print("\nFirst 3 snippets:\n")

for snippet in transcript[:3]:

    print("Text:", snippet.text)
    print("Start:", snippet.start)
    print("Duration:", snippet.duration)
    print("-" * 50)