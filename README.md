# Wikipedia Philosophy Game

A Python script that tests the "Getting to Philosophy" phenomenon on Wikipedia.

## The Phenomenon

According to a widely-circulated internet myth, clicking the first link in the main text of any Wikipedia article, and then repeating the process for subsequent articles, will eventually lead you to the "Philosophy" page.

This script automates that process to test whether it's true!

## Inspiration

The idea for this project came from [this TikTok video](https://www.tiktok.com/@lukasg007/video/7498752547780414766) by @lukasg007.

## Features

- Interactive prompt for starting Wikipedia page
- Follows the first valid link in each article's main content
- Skips links in parentheses and italics (following Wikipedia's actual pattern)
- Detects loops and attempts to recover by trying the second link
- Verbose output showing each page visited
- Comprehensive summary with full path and statistics

## Installation

1. Clone or download this repository

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python wikipedia_philosophy.py
```

The script will prompt you to enter a Wikipedia page title. Enter any topic (e.g., "Dog", "Computer", "Basketball") and press Enter.

Example:

```
Enter a Wikipedia page title (e.g., 'Dog', 'Python'): Dog
```

The script will then:
1. Fetch the Wikipedia page
2. Find the first valid link in the main article content
3. Navigate to that page
4. Repeat until reaching "Philosophy" or encountering an error

## How It Works

The script follows these rules to find the "first link":

1. **Main content only**: Only considers links in the main article body
2. **Skip parentheses**: Ignores links within parenthetical statements
3. **Skip italics**: Ignores italicized links (often self-references)
4. **Skip special pages**: Ignores Wikipedia meta pages (Help:, Wikipedia:, etc.)
5. **Skip citations**: Ignores reference and citation links

If a loop is detected (visiting the same page twice), the script will backtrack and try the second valid link from the previous page.

## Example Output

```
🌐 Wikipedia Philosophy Game
============================================================
Enter a Wikipedia page title (e.g., 'Dog', 'Python'): Dog

🎯 Starting from: Dog
🎯 Target: Philosophy
────────────────────────────────────────────────────────────
1. Dog
2. Domestication
3. Mutualism_(biology)
4. Symbiosis
5. Interaction
6. Action_(philosophy)
7. Philosophy

✅ SUCCESS! Reached Philosophy!
────────────────────────────────────────────────────────────

📊 Summary:
   Total clicks: 7

📍 Path taken:
   1. Dog
   2. Domestication
   3. Mutualism_(biology)
   4. Symbiosis
   5. Interaction
   6. Action_(philosophy)
   7. Philosophy
```

## Limitations

- The script may not work for all Wikipedia pages (some pages have unusual structures)
- Wikipedia's HTML structure may change over time, potentially breaking the parser
- Some pages may lead to loops or dead ends
- The script respects a maximum of 500 iterations to prevent infinite loops

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- lxml

## License

This is a fun educational project. Feel free to use and modify as you wish!

## Contributing

Found a bug or have an improvement? Feel free to open an issue or submit a pull request!
