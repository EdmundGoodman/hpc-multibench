### Variables ###
# https://clarkgrubb.com/makefile-style-guide
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.DEFAULT_GOAL := default


.PHONY: default
default:
	@echo "Try installing the project with `make install`"

### Installation ###
.PHONY: install
install:
	@echo "Initialising project:"
	@poetry install
	@poetry run pre-commit install


### Static analysis ###
.PHONY: check
check: .venv/
	@echo "Running pre-commit hooks:"
	@poetry run pre-commit run --all-files

.PHONY: whitelist
whitelist:
	@echo "Creating vulture whitelist:"
	@echo "# noqa" > src/hpc_multibench/whitelist.py
	@echo "# type: ignore" >> src/hpc_multibench/whitelist.py
	@poetry run vulture src/hpc_multibench tests --make-whitelist \
		>> src/hpc_multibench/whitelist.py


### Testing ###
.PHONY: test_unit
test_unit: .venv/
	@echo "Running unit tests:"
	@poetry run coverage run -m pytest -s -m "not (integration)" &&\
 		poetry run coverage report -m

.PHONY: test_integration
test_integration: .venv/
	@echo "Running test_integration tests:"
	@poetry run coverage run -m pytest -s -m integration &&\
 		poetry run coverage report -m

.PHONY: test
test: .venv/
	@echo "Running tests:"
	@poetry run coverage run -m pytest -s &&\
 		poetry run coverage report -m

.PHONY: verify
verify: check test


### Execution ###
.PHONY: run
run: .venv/
	@echo "Run: 'poetry run python3 -m hpc_multibench yaml_examples/kudu_plan.yaml'"
# @poetry run python3 -m hpc_multibench


### Documentation ###
.PHONY: uml
uml: .venv/
	@echo "Generating UML diagrams"
	@cd docs/assets/images/ &&\
		rm -rf uml && mkdir uml/
	@cd docs/assets/images/uml &&\
		poetry run pyreverse \
			-o png -p hpc-multibench \
			--ignore plot,tui \
			../../../../src/hpc_multibench

# Broken by ellipsis in pydantic model definition
# @cd docs/assets/images/uml &&\
# 	poetry run erdantic hpc_multibench.yaml_model.TestPlanModel -o yaml_model.png

.PHONY: docs
docs: .venv/
	@echo "Generating documentation:"
	@poetry run mkdocs build --strict

.PHONY: view_docs
view_docs: site/index.html
	@echo "Opening documentation:"
	@xdg-open site/index.html


### Cleanup ###
.PHONY: clean_cache
clean_cache:
	@echo "Deleting tooling cache files:"
	rm -rf .mypy_cache/ .pytest_cache/ .ruff_cache/  .coverage

.PHONY: clean_docs
clean_docs:
	@echo "Deleting generated documentation site:"
	rm -rf site/

.PHONY: clean_pycache
clean_pycache:
	@echo "Deleting python cache files:"
	find . -not -path "./.venv/*" | \
		grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | \
		xargs rm -rf

.PHONY: clean
clean: clean_cache clean_docs clean_pycache

.PHONY: clobber
clobber: clean
	@echo "Deleting virtual environment"
	rm -rf .venv/
