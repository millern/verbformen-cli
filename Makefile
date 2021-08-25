
format:
	poetry run black --experimental-string-processing tests verbformen_cli

lint: format
	poetry run flake8
	poetry run mypy tests verbformen_cli

test:
	poetry run pytest tests verbformen_cli