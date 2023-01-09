no: # Replace `Optional[T]` with `Union[T, None]`
	find regta -iname "*.py" | xargs python -m no_optional
	find tests -iname "*.py" | xargs python -m no_optional
isort: # Sort import statements
	isort .
lint: # Check code quality
	flake8
	find . -iname "*.py" -not -path "./.venv/*" | xargs pylint
	mypy regta
test: # Run tests
	pytest
html_docs: # Build html docs
	cd docs/ && $(MAKE) clean && $(MAKE) html
