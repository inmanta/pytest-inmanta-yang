# Shortcuts for various dev tasks. Based on makefile from pydantic
.DEFAULT_GOAL := all
isort = isort tests src/pytest_inmanta_yang
black = black tests src/pytest_inmanta_yang
flake8 = flake8 tests src/pytest_inmanta_yang


.PHONY: install
install:
	pip install -U setuptools pip wheel
	pip install -U --pre -r requirements.dev.txt -e . -c requirements.txt

ci-install:
	PIP_INDEX_URL=https://packages.inmanta.com/public/quickstart/python/simple/ $(MAKE) install

.PHONY: format
format:
	$(isort)
	$(black)
	$(flake8)

.PHONY: pep8
pep8:
	$(flake8)

# Build up folders structure corresponding to inmanta loader structure, so mypy knows what goes where.
RUN_MYPY_TESTS=MYPYPATH=tests python -m mypy --html-report mypy/out/tests tests
RUN_MYPY_PIC=MYPYPATH=src python -m mypy --html-report mypy/out/pytest_inmanta_yang -p pytest_inmanta_yang

mypy-tests:
	@ echo -e "Running mypy on the module tests\n..."
	@ $(RUN_MYPY_TESTS)

mypy-piy:
	@ echo -e "Running mypy on pytest-inmanta-yang\n..."
	@ $(RUN_MYPY_PIC)

.PHONY: mypy
mypy: mypy-tests mypy-piy
