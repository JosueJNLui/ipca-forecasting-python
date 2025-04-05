{{ config(tags=['unit-test']) }}

{% call dbt_unit_testing.test ('selic', 'check_selic_data') %}

    {% call dbt_unit_testing.mock_source('external_source', 'tbl_selic') %}
        SELECT
            '01/01/2020' AS data
            , '0.67' AS valor

    {% endcall %}

    {% call dbt_unit_testing.expect() %}
        SELECT
            '2020-01-01'::date as date
            , 2020::smallint as year_partition
            , 0.67::numeric(5,2) as value

    {% endcall %}

{% endcall %}
