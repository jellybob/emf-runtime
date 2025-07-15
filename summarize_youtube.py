import os
from datetime import timedelta

import requests
from jinja2 import Template

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/"

EVENT_YEARS = [2012, 2014, 2016, 2018, 2022, 2024]  # Years with EMF events


def get_video_ids_for_year(year):
    """
    Fetches the schedule for a given year and extracts YouTube video IDs.
    """
    print(f"Getting schedule for {year}")
    url = f"https://emfcamp.org/schedule/{year}.json"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch schedule for year {year}: {resp.status_code}")
    data = resp.json()
    video_ids = []
    for event in data:
        video = event.get("video", {})
        youtube_url = video.get("youtube", None)
        if youtube_url is not None:
            video_id = youtube_url.split("v=")[-1].split("&")[0]
            video_ids.append(video_id)
    return video_ids


def get_all_video_ids():
    """
    Compiles a list of all YouTube video IDs from EMF event schedules.
    """
    all_video_ids = []
    for year in EVENT_YEARS:
        all_video_ids.extend(get_video_ids_for_year(year))
    return all_video_ids


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
    if not YOUTUBE_API_KEY:
        raise Exception(
            "Missing YOUTUBE_API_KEY environment variable."
        )
    video_ids = get_all_video_ids()
    total_seconds = get_total_duration(YOUTUBE_API_KEY, video_ids)
    days, hours, minutes = format_duration(total_seconds)
    html = render_html(days, hours, minutes, total_seconds, len(video_ids))
    with open("index.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
