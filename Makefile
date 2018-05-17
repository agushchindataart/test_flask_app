init:
	virtualenv get_aggregated_service/env -p python3
	get_aggregated_service/env/bin/pip install -r get_aggregated_service/requirements.txt
	get_aggregated_service/env/bin/pip install -r get_aggregated_service/requirements-dev.txt
	virtualenv put_aggregated_service/env -p python3
	put_aggregated_service/env/bin/pip install -r put_aggregated_service/requirements.txt
	put_aggregated_service/env/bin/pip install -r put_aggregated_service/requirements-dev.txt

clean:
	rm get_aggregated_service/env -R
	rm put_aggregated_service/env -R

run:
	PYTHONPATH=. get_aggregated_service/env/bin/python get_aggregated_service/application.py &
	PYTHONPATH=. put_aggregated_service/env/bin/python put_aggregated_service/application.py &

run_tests:
	PYTHONPATH=. get_aggregated_service/env/bin/pytest get_aggregated_service/tests
	PYTHONPATH=. put_aggregated_service/env/bin/pytest put_aggregated_service/tests

run_flake:
	PYTHONPATH=. get_aggregated_service/env/bin/flake8 get_aggregated_service --config=get_aggregated_service/.flake8 --exclude=env
	PYTHONPATH=. put_aggregated_service/env/bin/flake8 put_aggregated_service --config=put_aggregated_service/.flake8 --exclude=env
