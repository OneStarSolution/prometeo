from pydantic import BaseModel


class Job(BaseModel):
    category: str
    location: str
    country: str
    source: str
