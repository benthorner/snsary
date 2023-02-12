bootstrap:
	pip install -e .
	pip install -r requirements/tests.txt
	pip install -r requirements/docs.txt

bootstrap-contrib-%:
	pip install -e .[$*]
	pip install -r requirements/$*/tests.txt

bootstrap-all: bootstrap
	pip install -e .[all]
	cat requirements/*/tests.txt | xargs pip install

test:
	black --check .
	isort --check-only .
	flake8 .
	pytest --ignore=tests/contrib

test-contrib-%:
	pytest tests/contrib/*$**

test-all: test
	pytest tests/contrib

lint-contrib:
	scripts/lint-contrib.sh

.PHONY: docs
docs:
	sphinx-autobuild --watch src docs/sphinx tmp/docs
