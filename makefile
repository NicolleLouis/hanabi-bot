start:
	cat instructions.txt
	poetry run python __main__.py

coverage:
	pytest --cov --cov-report=html
