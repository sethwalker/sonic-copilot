import string
import random
import hashlib


def generate_file_name(prefix, suffix, content):
    content_hash = hashlib.sha256(content.encode()).hexdigest()

    file_name = prefix + "_" + content_hash[:8] + "_" + suffix
    return file_name
