import re

async def get_game_emoji(type):
    if type == 1:
        return "🃏"
    elif type == 2:
        return "🎲"
    elif type == 3:
        return "🖐"
    
    return None

def remove_html_tags(text: str) -> str:
    """Remove HTML tags from a string"""
    return re.sub(r'<[^>]*>', '', text)