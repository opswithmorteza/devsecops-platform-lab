"""Narrow Dockerfile checks; not a full parser or vulnerability scanner."""
from pathlib import Path
import re
import sys


def check(text):
    lines = [x.strip() for x in text.splitlines() if x.strip() and not x.lstrip().startswith('#')]
    issues = []
    users = [x.split(None, 1)[1] for x in lines if x.upper().startswith('USER ')]
    if not users or users[-1].split(':')[0].lower() in {'root', '0'}:
        issues.append('Final USER must explicitly be non-root.')
    if not any(x.upper().startswith('HEALTHCHECK ') for x in lines):
        issues.append('Add a HEALTHCHECK.')
    for line in lines:
        if line.upper().startswith('FROM '):
            image = line.split()[1]
            if ':' not in image or image.endswith(':latest'):
                issues.append('Use an explicit base image version.')
        if re.search(r'(?:curl|wget).*\|\s*(?:sh|bash)', line):
            issues.append('Do not pipe downloaded scripts directly into a shell.')
    return issues


if __name__ == '__main__':
    errors = check(Path(sys.argv[1] if len(sys.argv) > 1 else 'Dockerfile').read_text())
    print('\n'.join(errors) if errors else 'Selected Dockerfile policies passed.')
    raise SystemExit(bool(errors))
