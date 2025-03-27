#!/bin/bash

ENV=$1;
JSON_PATH=$2;

if [[ "$ENV" == "dev" ]]
then
    S3_URI="s3://.............-assets/data_source/"
fi

read -p "Você tem certeza que quer subir esses arquivos em $ENV? (s/n)" permission

if [[ "$permission" == "s" ]]
then

    aws s3 cp $JSON_PATH  $S3_URI --profile $ENV;

else
    echo "Upload negado"
fi
