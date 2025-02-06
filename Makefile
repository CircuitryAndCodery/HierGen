
PYTHON=3.13
.PHONY: \
	install-pre-commit \
	install-editable \
	build \
	build-baseline \
	build-docs \
	check-mypy \
	check-pytest \
	check-pytest-cov \
	check-pydoclint \
	check-ruff-check \
	check-ruff-check-fix \
	check-ruff-check-fix-unsafe \
	check-ruff-format \
	check-pre-commit \
	git-commit-no-verify \
	uv-lock \
	clean 

sync:
	uv sync --dev

install-pre-commit:
	uvx pre-commit install

install-editable:
	uv pip install -e .

build:
	uv build

build-baseline:
	uvx --python=${PYTHON} pydoclint src --generate-baseline true --baseline baseline.txt

build-docs:
	uvx --python=${PYTHON} --with mkdocs-material --with mkdocstrings[python] mkdocs build

check-mypy:
	uvx --python=${PYTHON} mypy src

check-pytest:
	uvx --python=${PYTHON} pytest

check-pytest-cov:
	uvx --python=${PYTHON} --from pytest-cov pytest --cov --cov-report json:.coverage.json

check-pydoclint:
	uvx --python=${PYTHON} pydoclint src

check-ruff-check:
	uvx --python=${PYTHON} ruff check

check-ruff-check-fix:
	uvx --python=${PYTHON} ruff check --fix

check-ruff-check-fix-unsafe:
	uvx --python=${PYTHON} ruff check --fix --unsafe-fixes

check-ruff-format:
	uvx --python=${PYTHON} ruff format

check-pre-commit:
	uvx --python=${PYTHON} pre-commit run --all-files

uv-lock:
	rm -f uv-lock && uv pip install -e . && uv lock

git-commit-no-verify:
	git commit --no-verify