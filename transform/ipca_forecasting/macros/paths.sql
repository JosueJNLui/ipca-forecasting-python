{% macro external_json_path(filename) %}
{% set s3_path = 's3://personal-projects-landing' ~ '-' ~  env_var('ENV') ~ '-' ~ env_var('AWS_REGION') ~ '-' ~ env_var('AWS_ACCOUNT_ID') ~ '/' ~ env_var('BUCKET_PATH') ~ '/' ~ filename ~ '.json' %}
    '{{ s3_path }}'
{% endmacro %}

{% macro get_s3_path(layer, table_name) %}
{% set s3_path = 's3://personal-projects-' ~ layer ~ '-' ~  env_var('ENV') ~ '-' ~ env_var('AWS_REGION') ~ '-' ~ env_var('AWS_ACCOUNT_ID') ~ '/' ~ env_var('BUCKET_PATH') ~ '/' ~ table_name ~ '/*/*.parquet' %}
    '{{ s3_path }}'
{% endmacro %}
