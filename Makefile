cov-report = true

lint:
	pipenv run flake8 urouter
	pipenv run black -l 100 --check tests urouter

format:
	pipenv run black -l 100 tests urouter

install-dev:
	pipenv install --skip-lock -d

test:
	pipenv run coverage run -m pytest tests
	@if [ $(cov-report) = true ]; then\
    pipenv run coverage combine;\
    pipenv run coverage report;\
	fi

freeze:
	pipenv lcock -d