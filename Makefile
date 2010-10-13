test:
	@export PYTHONPATH=$$PYTHONPATH:. && nosetests -v -s --with-coverage --cover-erase --cover-inclusive --cover-package=cyrusbus