# Sudarshan Pathalam’s Personal Website

Source for my personal website, bringing together my infrastructure and data engineering background with experience across software engineering, technical marketing, product management, and solutions engineering.

Website address: [sudar-path.github.io](https://sudar-path.github.io/)

## What’s on the site

- A personal introduction and portrait.
- An overview of my background and the roles I’ve held.
- A featured public demo: [AIOps in Action: Predictive Maintenance & Anomaly Detection](https://videos.confluent.io/watch/4aLjWf4DRNXxdoi5Vg5XDB).
- A link to my [GitHub profile](https://github.com/sudar-path).

The site uses plain HTML and CSS. There are no JavaScript dependencies, external fonts, analytics, or build steps. The demo links to the recording rather than loading a third-party video embed.

## Preview locally

From the repository directory, run:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Press `Ctrl+C` to stop the server.

You can also open `index.html` directly in a browser.

## Project structure

```text
index.html          Homepage content and navigation
styles.css          Responsive layout, colors, and typography
assets/
  portrait.jpg      Cropped, lightly brightened portrait, without EXIF metadata
  favicon.svg       Site icon
tests/
  test_site.py      Dependency-free content and link checks
```

## Make changes

1. Update the content in `index.html` or the design in `styles.css`.
2. Preview at desktop and mobile widths. Check navigation and keyboard focus.
3. Run the checks:

   ```bash
   python3 -m unittest discover -s tests -v
   ```

4. Review the changes before committing or publishing.

The experience section lists roles, not a chronological employment history. Add employers, dates, and further demo details only after confirming them.

## Publishing

GitHub Pages publishing is configured in this repository’s **Settings → Pages**. Verify the publishing branch or workflow there before deploying. Local changes do not update the public site until they are committed, pushed, and published.

The portrait is stored locally with the site. The page makes no third-party requests until a visitor follows an external link.
