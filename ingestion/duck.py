import duckdb


class DB:
    def __init__(self, aws_profile: str, aws_region: str):
        self.conn = duckdb.connect()
        self.aws_profile = aws_profile
        self.aws_region = aws_region

    def load_aws_credentials(self) -> None:
        self.conn.sql(f"""
            INSTALL aws;
            LOAD aws;
            CALL load_aws_credentials('{self.aws_profile}');
            SET s3_region='{self.aws_region}';
            """)

    def query_from_s3(self, s3_path: str) -> list[tuple]:
        self.load_aws_credentials()
        relation = self.conn.sql(f"""
            SELECT * FROM '{s3_path}';
            """)

        columns = relation.columns
        results = relation.fetchall()

        return columns, results
