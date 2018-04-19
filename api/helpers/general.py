"""
General helper functions.
"""

from hashlib import sha512


def is_substring(sub, main):
    """
    Check if a string is a substring of another.
    """
    sub, main = sub.lower(), main.lower()
    subs = []
    for i in range(0, len(main) - len(sub)):
        subs.append(main[i: i + len(sub)])
    if sub in subs:
        return True
    return False


def digest(string):
    """
    Return a SHA512 DIGEST OF A string.
    """
    return sha512(string.encode('utf-8')).hexdigest()
