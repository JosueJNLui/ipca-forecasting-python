include .env
export

DBT_FOLDER = transform/ipca_forecasting

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

data-transform:
	poetry run dbt run \
		--target dev \
		--project-dir $$DBT_FOLDER \
		--profiles-dir $$DBT_FOLDER

dbt-test:
	poetry run dbt test \
		--target dev \
		--project-dir $$DBT_FOLDER \
		--profiles-dir $$DBT_FOLDER