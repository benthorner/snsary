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

upload:
	python -m pip install --upgrade build twine
	python -m build
	python -m twine upload --skip-existing dist/*

tag:
	$(eval \
		VERSION = $(shell cat setup.py | grep 'version=' | cut -d '"' -f 2) \
	)

	if ! git ls-remote --tags --exit-code origin v$(VERSION); then \
		git tag v$(VERSION); \
		git push --tags; \
	fi
