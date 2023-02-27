setup:
	pip install -r requirements.txt

run:
	python3 main.py

test:
	coverage run -m pytest

clean:
	rm -rf __pycache__

pip_upgrade:
