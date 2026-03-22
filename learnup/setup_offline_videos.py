import os
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE, "static", "videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)

# Using a public domain small sample video to represent offline educational content
# Big Buck Bunny sample is extremely reliable and small for demonstrating custom HTML5 video
VIDEO_URL = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
VIDEO_PATH = os.path.join(VIDEOS_DIR, "educational_sample.mp4")

def main():
    print("Downloading offline video package...")
    if not os.path.exists(VIDEO_PATH):
        try:
            urllib.request.urlretrieve(VIDEO_URL, VIDEO_PATH)
            print(f"✅ Successfully downloaded sample MP4 to {VIDEO_PATH}")
        except Exception as e:
            print(f"❌ Failed to download video: {e}")
            # Create dummy payload if net fails
            with open(VIDEO_PATH, "wb") as f:
                f.write(b"dummy mp4 data")
    else:
        print(f"✅ Video already exists at {VIDEO_PATH}")

if __name__ == "__main__":
    main()
