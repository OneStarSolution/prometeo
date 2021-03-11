import os
import re
from fastapi import APIRouter


router = APIRouter()


def count_files(pattern: str, base_path="data/enhanced"):
    regex = re.compile(pattern)
    files_list = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if regex.match(file):
                files_list.append(file)
    return files_list


@router.get("/")
def count(pattern: str):
    return count_files(pattern)
