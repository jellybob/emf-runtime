# YouTube Summarizer

This project generates a static web page displaying the total runtime of all videos on a specified YouTube channel. It is designed to run automatically via GitHub Actions and deploys the result to GitHub Pages.

## Features

- Fetches all videos from a YouTube channel using the YouTube Data API
- Calculates the total runtime in days, hours, and minutes
- Generates a simple HTML summary page
- Automatically updates and deploys via GitHub Actions and GitHub Pages

## Setup

1. **Clone the repository**

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set environment variables**

   - `YOUTUBE_API_KEY`: Your YouTube Data API key
   - `YOUTUBE_CHANNEL_ID`: The channel ID to summarize

   You can use a `.env` file (not committed) or set these in your shell.

4. **Run locally**

   ```sh
   python summarize_youtube.py
   ```

   This will generate `index.html` in the project root.

## GitHub Actions

- The workflow in `.github/workflows/update-runtime.yml` runs on a schedule and on manual dispatch.
- It installs dependencies, runs the summarizer, commits changes to `index.html` if needed, and deploys to the `gh-pages` branch for GitHub Pages.
- Add your secrets (`YOUTUBE_API_KEY`, `YOUTUBE_CHANNEL_ID`) in the repository settings.

## Testing

Run the included tests with:

```sh
python -m unittest test_summarize_youtube.py
