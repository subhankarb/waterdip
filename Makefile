## Run pytest for the module tests
pytest:
	set -e
	set -x
	pytest -p no:warnings ./tests/*

pytest_with_coverage:
	set -e
	set -x
	pytest -p no:warnings --cov ./tests/*
# Start Waterdip server
start_wd_server:
	python -m waterdip