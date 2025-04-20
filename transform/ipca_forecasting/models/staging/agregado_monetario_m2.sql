WITH aux_cte AS (
    SELECT
        STRPTIME(data, '%d/%m/%Y')::DATE as date
        , valor::NUMERIC(15,2) as value
    FROM 
        {{ external_json_path('agregado_monetario_m2') }}
)
SELECT
    aux_cte.*
    , YEAR(date)::SMALLINT as year_partition
    , CAST(LPAD(CAST(MONTH(date) AS VARCHAR), 2, '0') || '-' || CAST(YEAR(date) AS VARCHAR) AS CHAR(7)) as month_year
FROM
    aux_cte
