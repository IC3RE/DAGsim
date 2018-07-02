init:
	pip3 install -r requirements.txt

test:
	python -m unittest discover

.PHONY: init test
