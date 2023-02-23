
from typing import List
from pydantic import BaseModel
from datetime import datetime


class Accession(BaseModel):
    adsh: str
    reportDate: datetime


class AccessionDto(BaseModel):
    ciks: str
    accessions: List[Accession] = []
