.PHONY: data-ingest format test

data-ingest:
	poetry run python -m ingestion.pipeline
format:
	ruff format .
test:
	pytest test
