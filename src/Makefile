.PHONY: init test lint dist

all: init test lint

init:
	pip3 install -r requirements.txt

init_test:
	pip3 install -r requirements_test.txt

lint:
	flake8 cockatoo_ai/

output_requirements:
	pipenv requirements > requirements.txt

output_test_requirements:
	pipenv requirements --dev > requirements_test.txt
