{{ config(tags=['unit-test']) }}

{% call dbt_unit_testing.test ('icc', 'check_icc_data') %}

    {% call dbt_unit_testing.mock_source('external_source', 'tbl_icc') %}
        SELECT
            '01/01/2020' AS data
            , '1234.56' AS valor

    {% endcall %}

    {% call dbt_unit_testing.expect() %}
        SELECT
            '2020-01-01'::date as date
            , 2020::smallint as year_partition
            , 1234.56::numeric(7,2) as value

    {% endcall %}

{% endcall %}
