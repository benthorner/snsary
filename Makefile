bootstrap:
	pip install -e .
	pip install -r requirements/test.txt

bootstrap-contrib-%:
	pip install -e .[$*]
	pip install -r requirements/$*/tests.txt

bootstrap-all: bootstrap
	pip install -e .[all]
	cat requirements/*/tests.txt | xargs pip install

test:
	isort --check-only .
	flake8 .
	pytest --ignore=tests/contrib

test-contrib-%:
	pytest tests/contrib/*$**

test-all: test
	pytest tests/contrib

.PHONY: docs
docs:
	sphinx-autobuild --watch src docs/sphinx tmp/docs
