from configparser import ConfigParser


def config(section, filename='config.ini'):
    parser = ConfigParser()
    parser.read(filename)
    p = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            p[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return p
