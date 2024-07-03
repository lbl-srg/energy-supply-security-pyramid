BPDOC=doc

PEP8_ARGS=--recursive --max-line-length=100 \
  --exclude="*/thirdParty/*" \
  --ignore="E402" \
  --aggressive --aggressive --aggressive \
  maslow


.PHONY: doc clean

doc:
	@echo "*** Generating documentation"
	(cd $(BPDOC); make html linkcheck)

pep8:
ifeq ($(PEP8_CORRECT_CODE), true)
	@echo "*** Running autopep8 to correct code"
	autopep8 --in-place $(PEP8_ARGS)
	@echo "*** Checking for required code changes (apply with 'make pep8 PEP8_CORRECT_CODE=true')"
	git diff --exit-code .
else
	@echo "*** Checking for required code changes (apply with 'make pep8 PEP8_CORRECT_CODE=true')"
	autopep8 --diff $(PEP8_ARGS)
endif

doctest:
	python3 -m doctest \
	math/*.py

unittest:
	python3 -m unittest discover maslow/tests

