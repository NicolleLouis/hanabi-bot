single:
	python __main__.py -bot 1

multi:
	python __main__.py -multi True -number 4

coverage:
	pytest --cov --cov-report=html
