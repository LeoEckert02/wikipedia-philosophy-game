# Wikipedia Philosophy Game

A Python script that tests the "Getting to Philosophy" phenomenon on Wikipedia.

## The Phenomenon

According to a widely-circulated internet myth, clicking the first link in the main text of any Wikipedia article, and then repeating the process for subsequent articles, will eventually lead you to the "Philosophy" page.

This script automates that process to test whether it's true!

## Inspiration

The idea for this project came from [this TikTok video](https://www.tiktok.com/@lukasg007/video/7498752547780414766) by @lukasg007.

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
============================================================
🌐 Wikipedia Philosophy Game
============================================================
Enter a Wikipedia page title (e.g., 'Dog', 'Python'): Computer

🎯 Starting from: Computer
🎯 Target: Philosophy
────────────────────────────────────────────────────────────
1. Computer
2. Machine
3. Thermodynamic_system
4. Matter
5. Classical_physics
6. Scientific_theory
7. Universe
8. Space
9. Three-dimensional_space
10. Geometry
11. Mathematics
12. Empirical_sciences
13. Hypotheses
14. Explanation
15. Proposition
16. Philosophy_of_language

✅ SUCCESS! Reached Philosophy!
────────────────────────────────────────────────────────────

📊 Summary:
   Total clicks: 16

📍 Path taken:
   1. Computer
   2. Machine
   3. Thermodynamic_system
   4. Matter
   5. Classical_physics
   6. Scientific_theory
   7. Universe
   8. Space
   9. Three-dimensional_space
   10. Geometry
   11. Mathematics
   12. Empirical_sciences
   13. Hypotheses
   14. Explanation
   15. Proposition
   16. Philosophy_of_language
   17. Philosophy
```



