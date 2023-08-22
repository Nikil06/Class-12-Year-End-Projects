from .helper import parse_encoded_text

def printc(*args, sep=' ', end='\n', remove_tags=False):
    text = sep.join(map(str, args))
    text = parse_encoded_text(text, remove_tags)
    print(text, end=end)

