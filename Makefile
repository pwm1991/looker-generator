setup:
	pip install -r requirements.txt

run:
	python3 main.py

test:
	coverage run -m pytest

auth:
	gcloud auth application-default login

clean:
	rm -rf __pycache__ .pytest_cache .coverage

pip_upgrade:
	sudo pip3 install pip --upgrade
