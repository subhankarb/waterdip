## Run pytest for the module tests
pytest:
	set -e
	set -x
	pytest -p no:warnings ./tests/*

pytest_with_coverage:
	set -e
	set -x
	coverage run -m pytest -p no:warnings ./tests/*
# Start Waterdip server
start_wd_server:
	python -m waterdip