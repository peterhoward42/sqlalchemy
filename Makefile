.PHONY: all
all: mypy rufflint ruffmt test

.PHONY: rufflint
rufflint:
	ruff check --fix

.PHONY: ruffmt
ruffmt:
	ruff format .

.PHONY: mypy
mypy:
	mypy .

.PHONY: test
test:
	pytest