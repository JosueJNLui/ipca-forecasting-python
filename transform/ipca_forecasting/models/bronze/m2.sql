SELECT
    strptime(data, '%d/%m/%Y')::date as date
    , year(strptime(data, '%d/%m/%Y'))::smallint as year_partition
    , valor::numeric(15,2) as value
FROM 
    {{ dbt_unit_testing.source('external_source', 'tbl_m2') }}