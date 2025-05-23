{{ config(tags=['unit-test']) }}

{% call dbt_unit_testing.test ('m2', 'check_m2_data') %}

    {% call dbt_unit_testing.mock_source('external_source', 'tbl_m2') %}
        SELECT
            '01/01/2020' AS data
            , '65678178000.00' AS valor

    {% endcall %}

    {% call dbt_unit_testing.expect() %}
        SELECT
            '2020-01-01'::date as date
            , 2020::smallint as year_partition
            , 65678178000.00::numeric(15,2) as value

    {% endcall %}

{% endcall %}
