#!/usr/bin/env python3
"""
Wikipedia Philosophy Game
Tests the phenomenon that clicking the first link in a Wikipedia article
eventually leads to the Philosophy page.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import sys


class WikipediaPhilosophyGame:
    """Navigate Wikipedia links to reach Philosophy"""

    BASE_URL = "https://en.wikipedia.org"
    TARGET = "Philosophy"
    MAX_ITERATIONS = 500  # Prevent infinite loops

    def __init__(self):
        self.visited_pages = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Wikipedia Philosophy Game/1.0)'
        })

    def get_page_title_from_url(self, url):
        """Extract the page title from a Wikipedia URL"""
        path = urlparse(url).path
        if '/wiki/' in path:
            title = path.split('/wiki/')[-1]
            return unquote(title)
        return None

    def fetch_page(self, page_title):
        """Fetch a Wikipedia page by title"""
        url = f"{self.BASE_URL}/wiki/{page_title}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text, url
        except requests.RequestException as e:
            print(f"❌ Error fetching page: {e}")
            return None, None

    def is_valid_link(self, link):
        """Check if a link is valid for following"""
        if not link or not link.get('href'):
            return False

        href = link.get('href', '')

        # Must be a wiki article link
        if not href.startswith('/wiki/'):
            return False

        # Skip special pages
        invalid_prefixes = [
            '/wiki/Help:',
            '/wiki/Wikipedia:',
            '/wiki/Special:',
            '/wiki/Talk:',
            '/wiki/File:',
            '/wiki/Template:',
            '/wiki/Category:',
            '/wiki/Portal:',
        ]

        if any(href.startswith(prefix) for prefix in invalid_prefixes):
            return False

        # Skip citations and references
        if '#cite' in href or href.startswith('#'):
            return False

        return True

    def is_in_parentheses(self, element):
        """Check if an element is inside parentheses in the text"""
        # Walk up the tree to check for parenthetical context
        current = element
        while current:
            if current.name == 'p':
                # Found the paragraph, now check the text context
                text = current.get_text()
                link_text = element.get_text()

                # Simple approach: check if link appears within parentheses
                # This is a heuristic and may not catch all cases
                pattern = r'\([^)]*' + re.escape(link_text) + r'[^)]*\)'
                if re.search(pattern, text):
                    return True
                break
            current = current.parent
        return False

    def is_in_italics(self, element):
        """Check if an element is in italics"""
        current = element
        while current:
            if current.name in ['i', 'em']:
                return True
            if current.name == 'p':
                break
            current = current.parent
        return False

    def find_first_valid_links(self, html, num_links=2):
        """Find the first valid link(s) in the main article content"""
        soup = BeautifulSoup(html, 'lxml')

        # Find the main content area
        content = soup.find('div', {'id': 'mw-content-text'})
        if not content:
            return []

        # Find the main article body (first div with class 'mw-parser-output')
        article_body = content.find('div', {'class': 'mw-parser-output'})
        if not article_body:
            return []

        valid_links = []

        # Look through paragraphs in order
        for paragraph in article_body.find_all('p', recursive=False):
            # Skip empty paragraphs
            if not paragraph.get_text(strip=True):
                continue

            # Process the paragraph text to handle parentheses properly
            # We'll remove content in parentheses and then find links
            p_html = str(paragraph)

            # Find all links in this paragraph
            links = paragraph.find_all('a', href=True)

            for link in links:
                if not self.is_valid_link(link):
                    continue

                # Skip links in italics (usually references to the article itself)
                if self.is_in_italics(link):
                    continue

                # Skip links in parentheses (more sophisticated check)
                if self.is_in_parentheses(link):
                    continue

                # This is a valid link
                href = link['href']
                full_url = urljoin(self.BASE_URL, href)
                valid_links.append(full_url)

                if len(valid_links) >= num_links:
                    return valid_links

        return valid_links

    def navigate(self, start_page):
        """Navigate from start_page trying to reach Philosophy"""
        current_page = start_page
        iteration = 0
        link_attempt = 0  # Track which link we're trying (0 = first, 1 = second)

        print(f"\n🎯 Starting from: {current_page}")
        print(f"🎯 Target: {self.TARGET}")
        print("─" * 60)

        while iteration < self.MAX_ITERATIONS:
            iteration += 1

            # Check if we've reached Philosophy
            if current_page == self.TARGET:
                print(f"\n✅ SUCCESS! Reached {self.TARGET}!")
                self.print_summary()
                return True

            # Check if we've visited this page before (loop detection)
            if current_page in self.visited_pages:
                print(f"\n🔄 Loop detected! Already visited '{current_page}'")

                if link_attempt == 0:
                    # Try the second link from the previous page
                    print("💡 Trying second link from previous page...")
                    link_attempt = 1

                    # Go back to previous page
                    if len(self.visited_pages) >= 1:
                        # Remove the current page from visited (we'll re-add it if needed)
                        current_page = self.visited_pages[-1]
                        continue
                    else:
                        print("❌ Cannot backtrack, no previous page")
                        return False
                else:
                    print("❌ Loop detected even with second link")
                    return False

            # Add to visited pages
            self.visited_pages.append(current_page)
            print(f"{iteration}. {current_page}")

            # Fetch the page
            html, url = self.fetch_page(current_page)
            if not html:
                print(f"❌ Failed to fetch page: {current_page}")
                return False

            # Find valid links (get both first and second if available)
            valid_links = self.find_first_valid_links(html, num_links=2)

            if not valid_links:
                print(f"❌ No valid links found on '{current_page}'")
                return False

            # Choose which link to follow based on link_attempt
            if link_attempt == 1 and len(valid_links) > 1:
                # Use second link
                next_url = valid_links[1]
                print(f"   → Following second link...")
                link_attempt = 0  # Reset for next page
            else:
                # Use first link
                next_url = valid_links[0]
                link_attempt = 0  # Reset for next page

            # Get the next page title
            next_page = self.get_page_title_from_url(next_url)
            if not next_page:
                print(f"❌ Could not parse page title from URL: {next_url}")
                return False

            current_page = next_page

        print(f"\n❌ Reached maximum iterations ({self.MAX_ITERATIONS})")
        return False

    def print_summary(self):
        """Print a summary of the journey"""
        print("─" * 60)
        print(f"\n📊 Summary:")
        print(f"   Total clicks: {len(self.visited_pages)}")
        print(f"\n📍 Path taken:")
        for i, page in enumerate(self.visited_pages, 1):
            print(f"   {i}. {page}")
        print(f"   {len(self.visited_pages) + 1}. {self.TARGET}")


def main():
    """Main entry point"""
    print("=" * 60)
    print("🌐 Wikipedia Philosophy Game")
    print("=" * 60)
    print("\nThis script tests the myth that clicking the first link")
    print("on any Wikipedia page will eventually lead to Philosophy.")
    print()

    # Get starting page from user
    start_page = input("Enter a Wikipedia page title (e.g., 'Dog', 'Python'): ").strip()

    if not start_page:
        print("❌ No page title provided")
        sys.exit(1)

    # Create game instance and start navigation
    game = WikipediaPhilosophyGame()
    success = game.navigate(start_page)

    if not success:
        print("\n📊 Partial path taken:")
        for i, page in enumerate(game.visited_pages, 1):
            print(f"   {i}. {page}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
