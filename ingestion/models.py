from pydantic import BaseModel, Field
from typing import List, Optional, Union, Annotated


class BCBJobParameters(BaseModel):
    start_date: str = "01/01/1999"
    end_date: str = "01/01/2025"
    format: str = "json"
    code: int
    table_name: str
    # destination: Annotated[Union[List[str], str], Field(default=["local"])]
    # s3_path: Optional[str]
    # aws_profile: Optional[str]


class SidraJobParameters(BaseModel):
    code: str
    table_name: str
    # destination: Annotated[Union[List[str], str], Field(default=["local"])]
    # s3_path: Optional[str]
    # aws_profile: Optional[str]
