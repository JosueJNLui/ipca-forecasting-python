from pydantic import BaseModel


class ForecastJobParameters(BaseModel):
    aws_profile: str
    aws_account_id: str
    aws_region: str
    env: str
