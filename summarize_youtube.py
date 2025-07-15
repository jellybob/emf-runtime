import os
from datetime import timedelta

import requests
from jinja2 import Template

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID")

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/"


def get_all_video_ids(api_key, channel_id):
    video_ids = []
    url = f"{YOUTUBE_API_URL}search?key={api_key}&channelId={channel_id}&part=id&maxResults=50&order=date&type=video"
    while url:
        resp = requests.get(url)
        data = resp.json()
        video_ids += [
            item["id"]["videoId"]
            for item in data.get("items", [])
            if "videoId" in item["id"]
        ]
        next_page = data.get("nextPageToken")
        if next_page:
            url = f"{YOUTUBE_API_URL}search?key={api_key}&channelId={channel_id}&part=id&maxResults=50&order=date&type=video&pageToken={next_page}"
        else:
            url = None
    return video_ids


def get_total_duration(api_key, video_ids):
    total_seconds = 0
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        ids = ",".join(batch)
        url = f"{YOUTUBE_API_URL}videos?key={api_key}&id={ids}&part=contentDetails"
        resp = requests.get(url)
        data = resp.json()
        for item in data.get("items", []):
            duration = item["contentDetails"]["duration"]
            total_seconds += parse_iso8601_duration(duration)
    return total_seconds


def parse_iso8601_duration(duration):
    import isodate

    return int(isodate.parse_duration(duration).total_seconds())


def format_duration(seconds):
    td = timedelta(seconds=seconds)
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return days, hours, minutes


def render_html(days, hours, minutes, total_seconds, video_count):
    template = Template("""
    <html>
    <head><title>YouTube Channel Total Runtime</title></head>
    <body>
        <h1>Total Runtime</h1>
        <p>{{ days }} days, {{ hours }} hours, {{ minutes }} minutes</p>
        <p>({{ total_seconds }} seconds)</p>
        <h2>Total Videos</h2>
        <p>{{ video_count }} videos</p>
    </body>
    </html>
    """)
    return template.render(
        days=days,
        hours=hours,
        minutes=minutes,
        total_seconds=total_seconds,
        video_count=video_count,
    )


def main():
    if not YOUTUBE_API_KEY or not CHANNEL_ID:
        raise Exception(
            "Missing YOUTUBE_API_KEY or YOUTUBE_CHANNEL_ID environment variable."
        )
    video_ids = get_all_video_ids(YOUTUBE_API_KEY, CHANNEL_ID)
    total_seconds = get_total_duration(YOUTUBE_API_KEY, video_ids)
    days, hours, minutes = format_duration(total_seconds)
    html = render_html(days, hours, minutes, total_seconds, len(video_ids))
    with open("index.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
