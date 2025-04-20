SELECT
    ipca.date
    , ipca.month_year
    , ipca.year_partition
    , ipca.value ipca_value
    , alimentacao_e_bebidas.value alimentacao_e_bebidas_value
    , habitacao.value habitacao_value
    , artigos_de_residencia.value artigos_de_residencia_value
    , vestuario.value vestuario_value
    , transporte.value transporte_value
    , comunicacao.value comunicacao_value
    , saude_e_cuidados_pessoais.value saude_e_cuidados_pessoais_value
    , despesas_pessoais.value despesas_pessoais_value
    , educacao.value educacao_value
    , comercializaveis.value comercializaveis_value
    , nao_comercializaveis.value nao_comercializaveis_value
    , precos_monitorados_total.value precos_monitorados_total_value
    , nucleo.value nucleo_value
    , bens_nao_duraveis.value bens_nao_duraveis_value
    , bens_semi_duraveis.value bens_semi_duraveis_value
    , duraveis.value duraveis_value
    , servicos.value servicos_value
    , selic_acumulada_ao_mes.value selic_acumulada_ao_mes_value
    , agregado_monetario_m2.value agregado_monetario_m2_value
    , indice_de_confianca_do_consumidor.value indice_de_confianca_do_consumidor_value
FROM
    {{ get_s3_path('bronze', 'ipca') }} ipca
    INNER JOIN {{ get_s3_path('bronze', 'alimentacao_e_bebidas') }} alimentacao_e_bebidas ON alimentacao_e_bebidas.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'habitacao') }} habitacao ON habitacao.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'artigos_de_residencia') }} artigos_de_residencia ON artigos_de_residencia.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'vestuario') }} vestuario ON vestuario.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'transporte') }} transporte ON transporte.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'comunicacao') }} comunicacao ON comunicacao.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'saude_e_cuidados_pessoais') }} saude_e_cuidados_pessoais ON saude_e_cuidados_pessoais.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'despesas_pessoais') }} despesas_pessoais ON despesas_pessoais.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'educacao') }} educacao ON educacao.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'comercializaveis') }} comercializaveis ON comercializaveis.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'nao_comercializaveis') }} nao_comercializaveis ON nao_comercializaveis.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'precos_monitorados_total') }} precos_monitorados_total ON precos_monitorados_total.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'nucleo') }} nucleo ON nucleo.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'bens_nao_duraveis') }} bens_nao_duraveis ON bens_nao_duraveis.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'bens_semi_duraveis') }} bens_semi_duraveis ON bens_semi_duraveis.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'duraveis') }} duraveis ON duraveis.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'servicos') }} servicos ON servicos.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'selic_acumulada_ao_mes') }} selic_acumulada_ao_mes ON selic_acumulada_ao_mes.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'agregado_monetario_m2') }} agregado_monetario_m2 ON agregado_monetario_m2.month_year = ipca.month_year
    INNER JOIN {{ get_s3_path('bronze', 'indice_de_confianca_do_consumidor') }} indice_de_confianca_do_consumidor ON indice_de_confianca_do_consumidor.month_year = ipca.month_year