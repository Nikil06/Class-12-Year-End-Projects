import re
from . import constants as c

def get_codes_from_tags(tags: list[str]) -> str:
    codes = []
    has_colours = False
    for tag in tags:
        if tag in c.colours:
            has_colours = True

        if tag in c.tag_map:
            codes.append(c.tag_map[tag])
        else:
            raise ValueError(f"The tag '{tag}' does not exist in the tag map.")

    if not has_colours:
        codes.append(c.reset_colours)

    return ''.join(codes)

def handle_tags(_tags: list[str], _active_tags: list[str]):
    tags = _tags.copy()
    active_tags = _active_tags.copy()

    for tag in tags:
        tag = tag.strip()

        if not tag:
            # Tag is empty
            continue

        if tag.startswith('/'):
            # Given tag is a closing tag

            tag = tag[1:]   # remove '/'

            if tag in active_tags:
                active_tags.remove(tag)
            # Ignore if it's a closing tag not in active_tags

        else:
            # Given tag is an opening tag
            if tag in c.tag_map:
                active_tags.append(tag)
            else:
                raise ValueError(f"The tag '{tag}' is an invalid tag.")

    return active_tags

def parse_encoded_text(text: str, remove_tags: bool):
    segments = re.split(r'(\[[^]]+])', text)
    f_segments = []
    active_tags = []

    for i, segment in enumerate(segments):
        if i % 2 == 0:
            # It's normal text
            f_segments.append(segment)
        else:
            # It's a tag segment
            if remove_tags:
                if not segment.startswith('[') or not segment.endswith(']'):
                    # Skip invalid tags in remove_tags mode
                    continue
            if f_segments[-1].endswith('/'):
                f_segments[-1] = f_segments[-1][:-1]
                f_segments.append(segment)
            elif not remove_tags:
                tags = segment[1:-1].split(',')
                active_tags = handle_tags(tags, active_tags)
                _segment = get_codes_from_tags(active_tags)
                f_segments.append(_segment)
    f_segments.append(c.reset)
    return ''.join(f_segments)
