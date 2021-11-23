import re
import string
from pathlib import Path


def _fix_name(s: str) -> str:
    return s.replace(' ', '_').translate(str.maketrans(string.punctuation, '_'*len(string.punctuation)))


def to_snake_case(s: str) -> str:
    s = _fix_name(s)
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower().replace('__', '_')


def to_camel_case(s: str) -> str:
    s = _fix_name(s)
    return ''.join(word.title() for word in s.split('_'))


def add_init_file(path: Path):
    init_path = path / "__init__.py"
    init_path.touch(exist_ok=True)
