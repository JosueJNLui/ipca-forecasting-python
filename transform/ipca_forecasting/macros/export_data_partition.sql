{% macro export_data_partition(layer, partition_col, table) %}
{% set s3_path = 's3://personal-projects-' ~ layer ~ '-' ~  env_var('ENV') ~ '-' ~ env_var('AWS_REGION') ~ '-' ~ env_var('AWS_ACCOUNT_ID') ~ '/' ~ env_var('BUCKET_PATH') %}
    COPY (
        SELECT 
            *
        FROM
            {{ table }}
    )
    TO '{{ s3_path }}/{{ table }}'
    (FORMAT PARQUET, PARTITION_BY ({{ partition_col }}), OVERWRITE_OR_IGNORE 1, COMPRESSION 'ZSTD');
{% endmacro %}
