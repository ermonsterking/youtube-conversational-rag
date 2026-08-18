from utils.youtube import extract_video_id


urls = [
    "https://www.youtube.com/watch?v=kFHSf2oS5l0",
    "https://youtu.be/kFHSf2oS5l0",
    "kFHSf2oS5l0",
]


for url in urls:

    video_id = extract_video_id(url)

    print(f"{url}")
    print(f"Video ID: {video_id}")
    print()