from fastapi import APIRouter
from typing import List
from pydantic import BaseModel


class Zipcodes(BaseModel):
    zipcodes: List[str]


router = APIRouter()


def create_file(data: list, base_path="data/enhanced"):
    with open("redistribution.csv", "w") as f:
        f.writelines(data)


@router.post("/")
def distribute(data: list):
    return create_file(data)
