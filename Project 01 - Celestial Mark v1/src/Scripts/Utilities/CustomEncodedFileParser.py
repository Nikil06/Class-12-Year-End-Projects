def read_encoded_file(file_path):
    """Reads the contents of the encoded file and returns a list of lines."""
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    return lines

def filter_lines(lines):
    """Filters out empty lines and lines starting with '#' from a list of lines and returns the filtered list."""
    ret_lines = []
    for line in lines:
        if line.strip() != '' and line[0] != '#':
            ret_lines.append(line[:-1])
    return ret_lines


def extract_sections(lines):
    """Extracts sections from the lines based on the '$$$' delimiter and returns a dictionary of sections."""
    current_section = ''
    current_section_first_idx = None
    sections = {}

    for i in range(len(lines)):
        if lines[i][:4] == '$$$ ':
            if current_section_first_idx is None:
                current_section = lines[i][4:]
                current_section_first_idx = i + 1
            else:
                sections[current_section] = lines[current_section_first_idx:i]
                current_section = lines[i][4:]
                current_section_first_idx = i + 1
        if i == len(lines) - 1 and current_section_first_idx is not None:
            sections[current_section] = lines[current_section_first_idx:]

    return sections


def parse_encoded_file(file_path):
    """Parses the encoded file and returns its sections as a dictionary."""
    file_lines = read_encoded_file(file_path)
    file_lines = filter_lines(file_lines)
    sections = extract_sections(file_lines)
    return sections

def get_section_data(file_path, section_title, return_list=False, return_str=False):
    """Retrieves a specific section from the parsed encoded file and returns it in the specified format. """
    parsed_data = parse_encoded_file(file_path)
    section = None
    try:
        section = parsed_data[section_title]
    except KeyError:
        raise KeyError('{} Section Unavailable in Encoded File'.format(section_title))

    if return_list and not return_str:
        return section
    elif return_str and not return_list:
        return '\n'.join(section)
    else:
        if not return_list and not return_str:
            raise TypeError('Return type has not been specified.')
        elif return_str and return_list:
            raise TypeError('Can only return list or str types, not both.')
