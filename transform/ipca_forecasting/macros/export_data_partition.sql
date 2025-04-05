{% macro export_data_partition(partition_col, table) %}
{% set s3_path = env_var('S3_BRONZE_BUCKET') ~ '/' ~ env_var('bucket-path') %}
    COPY (
        SELECT 
            *
        FROM
            {{ table }}
    )
    TO '{{ s3_path }}/{{ table }}'
    (FORMAT PARQUET, PARTITION_BY ({{ partition_col }}), OVERWRITE_OR_IGNORE 1, COMPRESSION 'ZSTD');
{% endmacro %}
