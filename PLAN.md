# YouTube Summarizer

This tool is designed to generate a single web page, which displays the total runtime of a
YouTube channel's videos. The tool is implemented in Python, running under Github Actions
it makes use of YouTube's API to collect the runtime and generate a single web page which
displays that runtime in days, hours, and minutes. That web page is served as a website
via Github Pages. You'll probably need to make use of Github's API to create a fresh commit
with the new value, but only if that value has changed since the last run.

All secrets should be injected via environment variables.

The channel ID to collect videos from and the YouTube API key should be configured via
repository secrets.

## Implementation Plan

1. **Set Up Project Structure**
   - Create a Python script to fetch and process YouTube channel data.
   - Add requirements.txt for dependencies (e.g., requests, PyYAML, Jinja2).

2. **YouTube API Integration**
   - Use the YouTube Data API to fetch all videos for a given channel ID.
   - Accumulate the total runtime of all videos.
   - Convert the total runtime to days, hours, and minutes.

3. **Web Page Generation**
   - Use a template engine (e.g., Jinja2) to generate a static HTML page displaying the total runtime.

4. **GitHub Actions Workflow**
   - Create a GitHub Actions workflow to run the script on a schedule (e.g., daily).
   - Inject secrets (API key, channel ID) via repository secrets/environment variables.
   - Check if the generated value has changed since the last run.
   - If changed, commit and push the new HTML file to the repository.

5. **GitHub Pages Deployment**
   - Configure GitHub Pages to serve the generated HTML file from the appropriate branch/folder.

6. **Testing and Validation**
   - Test the script locally with sample data and environment variables.
   - Validate the workflow by triggering it manually and confirming correct updates.

7. **Documentation**
   - Document setup, configuration, and usage in the README.md file.

## TODO: Use the schedule JSON to source videos.

We can request schedule.json for each event, and use that to find only relevant videos,
mostly because the timings seem off.
