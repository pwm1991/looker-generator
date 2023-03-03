setup:
	pip install -r requirements.txt

freeze:
	pipreqs --force

run:
	python3 main.py

test:
	coverage run -m pytest

test_verbose:
	coverage run -m pytest -vv

test_report:
	make test; coverage html

auth:
	gcloud auth application-default login

clean:
	rm -rf __pycache__ .pytest_cache .coverage

pip_upgrade:
	sudo pip3 install pip --upgrade
