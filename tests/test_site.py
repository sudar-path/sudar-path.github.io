from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DEMO_URL = "https://videos.confluent.io/watch/4aLjWf4DRNXxdoi5Vg5XDB"
PROFILE_URL = "https://github.com/sudar-path"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.page = PageParser()
        cls.page.feed(cls.html)

    def test_page_metadata_and_main_landmark(self):
        elements = self.page.elements
        self.assertIn(("html", {"lang": "en"}), elements)
        self.assertTrue(any(tag == "meta" and attrs.get("name") == "viewport"
                            for tag, attrs in elements))
        self.assertTrue(any(tag == "meta" and attrs.get("name") == "description"
                            and attrs.get("content") for tag, attrs in elements))
        self.assertEqual(sum(tag == "h1" for tag, _ in elements), 1)
        self.assertEqual(sum(tag == "main" for tag, _ in elements), 1)
        self.assertIn("Sudarshan Pathalam", self.html)

    def test_local_links_assets_and_sections_exist(self):
        ids = [attrs["id"] for _, attrs in self.page.elements if "id" in attrs]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate HTML IDs")
        self.assertTrue({"home", "main", "about", "demo", "experience", "connect"} <= set(ids))
        for tag, attrs in self.page.elements:
            for attribute in ("src", "href"):
                value = attrs.get(attribute)
                if not value:
                    continue
                parsed = urlsplit(value)
                if parsed.scheme or parsed.netloc:
                    continue
                with self.subTest(tag=tag, reference=value):
                    if parsed.path:
                        self.assertTrue((ROOT / unquote(parsed.path)).is_file())
                    elif parsed.fragment:
                        self.assertIn(unquote(parsed.fragment), ids)

    def test_portrait_has_alt_text_and_explicit_dimensions(self):
        images = [attrs for tag, attrs in self.page.elements if tag == "img"]
        self.assertEqual(len(images), 1)
        portrait = images[0]
        self.assertEqual(portrait["src"], "assets/portrait.jpg")
        self.assertIn("Sudarshan", portrait.get("alt", ""))
        self.assertEqual((portrait.get("width"), portrait.get("height")), ("720", "720"))
        self.assertLess((ROOT / portrait["src"]).stat().st_size, 200_000)

    def test_demo_profile_and_role_content(self):
        links = [attrs.get("href") for tag, attrs in self.page.elements if tag == "a"]
        self.assertIn(DEMO_URL, links)
        self.assertIn(PROFILE_URL, links)
        for role in ("Software engineer", "Technical marketing engineer",
                     "Product manager", "Solutions engineer"):
            self.assertIn(role, self.html)

    def test_external_links_are_safe_and_assets_are_local(self):
        for tag, attrs in self.page.elements:
            with self.subTest(tag=tag, attrs=attrs):
                if attrs.get("target") == "_blank":
                    self.assertTrue({"noopener", "noreferrer"} <= set(attrs.get("rel", "").split()))
                if tag in {"img", "script", "iframe", "link"}:
                    resource = attrs.get("src") or attrs.get("href", "")
                    self.assertFalse(urlsplit(resource).scheme)
                    self.assertFalse(urlsplit(resource).netloc)
        self.assertFalse(any(tag in {"script", "iframe"} for tag, _ in self.page.elements))
        self.assertIn("prefers-reduced-motion: reduce", (ROOT / "styles.css").read_text())


if __name__ == "__main__":
    unittest.main()
