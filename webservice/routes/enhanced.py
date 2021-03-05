import os
import re
from fastapi import APIRouter


router = APIRouter()


def count_files(pattern: str, base_path="data/enhanced"):
    regex = re.compile(pattern)
    count = 0
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if regex.match(file):
                count += 1
    return count


@router.get("/")
def count(pattern: str):
    return count_files(pattern)
