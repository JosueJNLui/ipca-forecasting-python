import duckdb
import pyarrow as pa 

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

    def query_from_s3(self, s3_bucket: str) -> list[tuple]:
        self.load_aws_credentials()
        relation = self.conn.sql(f"""
            SELECT * FROM 's3://{s3_bucket}';
            """)

        columns = relation.columns
        results = relation.fetchall()

        return columns, results

    def write_to_s3(self, data: list[dict], s3_bucket: str, table_path: str, format_object: str, partition: str = None):
        self.load_aws_credentials()

        arrow_table = pa.Table.from_pylist(data)

        copy_command = f"""
            COPY (
                WITH cte_data as (
                SELECT
                    *
                    , year(strptime({partition}, '%d/%m/%Y')) year_partition
                FROM
                    arrow_table
                )
                SELECT * FROM cte_data
            )
            TO 's3://{s3_bucket}/{table_path}'
            (FORMAT PARQUET, PARTITION_BY (year_partition), OVERWRITE_OR_IGNORE 1, COMPRESSION 'ZSTD');
        """

        self.conn.sql(copy_command)
