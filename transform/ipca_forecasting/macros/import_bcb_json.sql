{% macro  import_bcb_json(file) %}

SELECT
    strptime(data, '%d/%m/%Y')::date as date
    , year(strptime(data, '%d/%m/%Y'))::smallint as year_partition
    , valor::numeric(7,2) as value
FROM 
    {{ external_json_path(file) }}

{% endmacro %}
