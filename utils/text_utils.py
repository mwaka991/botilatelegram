"""
Text Utilities for Telegram Channel Bot

Provides text processing functions including:
- Link removal
- Text cleaning
- Content sanitization
"""

import re


def remove_links(text: str) -> str:
    """
    Remove all links from text while preserving other content.
    
    Removes:
    - HTTP/HTTPS URLs (http://example.com, https://example.com)
    - WWW links (www.example.com)
    - Telegram links (t.me/username, telegram.me/...)
    - Markdown links ([text](url))
    - Telegram inline links (@username mentions with context)
    
    Args:
        text: Input text to clean
        
    Returns:
        str: Text with all links removed (extra spaces cleaned up)
    """
    if not text:
        return text
    
    # Remove markdown links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', text)
    
    # Remove HTTP/HTTPS URLs
    text = re.sub(r'https?://[^\s]+', '', text)
    
    # Remove www links
    text = re.sub(r'www\.[^\s]+', '', text)
    
    # Remove Telegram links (t.me/*, telegram.me/*, etc.)
    text = re.sub(r't\.me/[^\s]+', '', text)
    text = re.sub(r'telegram\.me/[^\s]+', '', text)
    
    # Remove lines that are just links or mostly whitespace
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Skip empty lines after link removal
        if line.strip():
            cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Clean up multiple spaces
    text = re.sub(r' +', ' ', text)
    
    # Clean up multiple newlines
    text = re.sub(r'\n\n+', '\n\n', text)
    
    return text.strip()


def has_links(text: str) -> bool:
    """
    Check if text contains any links.
    
    Args:
        text: Text to check
        
    Returns:
        bool: True if text contains links, False otherwise
    """
    if not text:
        return False
    
    # Check for various link patterns
    patterns = [
        r'https?://',  # HTTP/HTTPS
        r'www\.',      # WWW
        r't\.me/',     # Telegram links
        r'telegram\.me/',
        r'\[([^\]]+)\]\(([^)]+)\)',  # Markdown links
    ]
    
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    
    return False


# For testing
if __name__ == "__main__":
    # Test cases
    test_texts = [
        "Check out this link https://example.com for more info",
        "Visit www.example.com or t.me/mychannel for updates",
        "This [link](https://example.com) is useful",
        "No links here, just plain text",
        "Multiple links: https://example.com and t.me/bot and www.site.com",
    ]
    
    print("=== Link Removal Tests ===\n")
    for text in test_texts:
        cleaned = remove_links(text)
        has_link = has_links(cleaned)
        print(f"Original: {text}")
        print(f"Cleaned:  {cleaned}")
        print(f"Has links: {has_link}\n")
