lint:
	pipenv run flake8 router
	pipenv run black -l 100 --check tests router

format:
	pipenv run black -l 100 tests router

install-dev:
	pipenv install --skip-lock -d

test:
	pipenv run coverage run -m pytest tests
	@if [ $(cov-report) = true ]; then\
    pipenv run coverage combine;\
    pipenv run coverage report;\
	fi

_release:
	scripts/make_release

release: test _release

freeze:
	pipenv lock -d