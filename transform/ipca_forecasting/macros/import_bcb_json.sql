{% macro  import_bcb_json(file) %}

WITH aux_cte AS (
    SELECT
        STRPTIME(data, '%d/%m/%Y')::DATE as date
        , valor::NUMERIC(7,2) as value
    FROM 
        {{ external_json_path(file) }}
)
SELECT
    aux_cte.*
    , YEAR(date)::SMALLINT as year_partition
    , MONTH(date)::TINYINT as month
    , CAST(CAST(YEAR(date) AS VARCHAR) || '-' || LPAD(CAST(MONTH(date) AS VARCHAR), 2, '0')AS CHAR(7)) as month_year
FROM
    aux_cte

{% endmacro %}
