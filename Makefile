include .env
export

DBT_FOLDER = transform/ipca_forecasting
BRONZE_MODELS = staging.*
SILVER_MODELS = intermediate.*

.PHONY: data-ingest format test

data-ingest:
	poetry run python -m ingestion.pipeline \
		--aws_profile $$AWS_PROFILE \
		--aws_account_id $$AWS_ACCOUNT_ID \
		--aws_region $$AWS_REGION \
		--env $$ENV

format:
	ruff format .
test:
	pytest test

staging-transform:
	poetry run dbt run \
		--target dev \
		--models $$BRONZE_MODELS \
		--project-dir $$DBT_FOLDER \
		--profiles-dir $$DBT_FOLDER
	
intermediate-transform:
	poetry run dbt run \
		--target dev \
		--models $$SILVER_MODELS \
		--project-dir $$DBT_FOLDER \
		--profiles-dir $$DBT_FOLDER

dbt-test:
	poetry run dbt test \
		--target dev \
		--project-dir $$DBT_FOLDER \
		--profiles-dir $$DBT_FOLDER

forecast:
	poetry run python -m forecast_model.main \
		--aws_profile $$AWS_PROFILE \
		--aws_account_id $$AWS_ACCOUNT_ID \
		--aws_region $$AWS_REGION \
		--env $$ENV
