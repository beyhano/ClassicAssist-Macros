## Orc Speech Translator - By: Bur'Gar
## Translates Orcish to English from Say and [c chat while preserving context
## Also translates your own words so you can practice orcish to klomp umies with words.
## Please report issues to Bur'gar on Discord.
import sys
import re
import Misc
import Player
import Journal
from System import Random

# Create reverse dictionary for Orc to English translation
REVERSE_ORC = {orc: eng for eng, orc in {
    'acid': 'kulz',
    'archer': "olig'r",
    'arrow': 'lig',
    'axe': 'lusk',
    'axer': "lusk'r",
    'bad': 'nubhosh',
    'bandage': 'rag',
    'battlecry': 'hoowah!',
    'bear': 'buub',
    'big': 'beg',
    'bird': 'zog',
    'blood': 'grish',
    'bolt': 'xligz',
    'bow': 'olig',
    'crafter': 'makur',
    'crossbow': 'xolig',
    'curse': 'skah',
    'dagger': 'igg',
    'darkness': 'burzum',
    'dead': 'flat',
    'dragon': 'kulkodar',
    'earth': 'uzg',
    'eight': 'h gahk',
    'ettin': 'vagun',
    'feather': 'feddurz',
    'female orc': 'feurk',
    'fencer': "kigg'r",
    'fire': 'ghaash',
    'five': 'h',
    'fool': 'glob',
    'four': 'futh',
    'ghost': 'angath',
    'giant': 'vagun',
    'give': 'gib',
    'good': 'hosh',
    'gold/loot': 'shiniez',
    'goodbye': "gug'ye",
    'guildstone': 'rok',
    'hello': 'hullo',
    'hi': 'ug',
    'hit': 'klomp',
    'horse': 'fuud',
    'huge': 'badda',
    'human': 'oomie',
    'i': 'me',
    'ice': 'akul',
    'iron': 'jarn',
    'kill': 'klomp',
    'know': 'gruk',
    'kryss': 'kult',
    'land': 'uzg',
    'leather': 'leddurz',
    'liche': 'laffur',
    'light': 'juurz',
    'laugh': 'har',
    'lol': 'hoho',
    'lord': 'goth',
    'mace': 'womp',
    'macer': "womp'r",
    'male orc': 'urk',
    'me': 'meeb',
    'mother': 'momo',
    'mud': 'balt',
    'nine': 'hfuth',
    'no': 'nub',
    'ogre': 'drangu',
    'one': 'ash',
    'orc': 'urk',
    'pig': 'buub',
    'poison': 'tokshun',
    'potion': 'mojo wadur',
    'power': 'gothurz',
    'quest': 'kwezt',
    'reagent': 'weedz',
    'resurrection': 'flezhie',
    'rune': 'rok',
    'say': 'blah',
    'scimitar': 'zult',
    'seven': 'hdub',
    'sheep': 'bresh',
    'shield': "blok'r",
    'six': 'hash',
    'slave': 'snaga',
    'snake': 'gajarpan',
    'snow': 'bor',
    'speak': 'blah',
    'spear': 'kigg',
    'spider': 'takhbork',
    'stinking': 'pushdug',
    'swordsman': "zult'r",
    'talk': 'blah',
    'ten': 'hh',
    'thanks': 'rulg',
    'there': 'der',
    'three': 'gahk',
    'thunder': 'zgur',
    'trap': 'krimp',
    'tree': "r'hee",
    'troll': 'olog',
    'two': 'dub',
    'understand': 'gruk',
    'water': 'brugh',
    'wind': 'yula',
    'wolf': 'howlur',
    'wood': 'wuud',
    'wool': 'wuulz',
    'yes': 'yub',
    'you': 'lat',
    'zero': 'zuth',
}.items()}

def translate_from_orc(text):
    """Translate Orcish text to English while preserving context"""
    # Store original text for reference
    original_text = text
    
    # Convert to lowercase for matching but keep original case structure
    text_lower = text.lower()
    
    # Remove common Orcish interjections for cleaner translation
    text_lower = re.sub(r'\b(waaagh|urk|grr)!?\b', '', text_lower, flags=re.IGNORECASE)
    
    # Split into words
    words = text_lower.split()
    original_words = original_text.split()
    
    # Track which words were translated
    translations = {}
    
    # First pass: identify Orcish words and their translations
    for i, word in enumerate(words):
        stripped_word = word.strip('.,!?')
        # Use regex with word boundaries to match whole words only
        for orc_word in REVERSE_ORC.keys():
            if re.search(r'\b' + re.escape(orc_word) + r'\b', stripped_word):
                translations[i] = REVERSE_ORC[orc_word]
                break
    
    # If no translations were found, return None
    if not translations:
        return None
    
    # Replace Orcish words with their translations while keeping original structure
    result_words = []
    for i, orig_word in enumerate(original_words):
        if i in translations:
            result_words.append(translations[i])
        else:
            result_words.append(orig_word)
    
    return ' '.join(result_words)

def main():
    Misc.SendMessage("Orc Translator started!", 68)
    Journal.Clear()
    
    while True:
        # Check for any text in journal
        if Journal.Search("[C"):  # Looking for emote messages
            text = Journal.GetLineText("[C")
            # Skip the message if it starts with [C and has no translations
            if not text.startswith("[C"):  # Only process if it's not the [C command itself
                translation = translate_from_orc(text)
                if translation:
                    Player.HeadMessage(38, f"[{translation}]")
            Journal.Clear()
        
        # Also check regular chat
        if Journal.Search(""):  # Get any text
            text = Journal.GetLineText("")
            translation = translate_from_orc(text)
            if translation:
                Player.HeadMessage(38, f"[{translation}]")
            Journal.Clear()
        
        Misc.Pause(100)

if __name__ == "__main__":
    main()


