install:
	python -m pip install -r requirements.txt

backend:
	python run_backend.py

frontend:
	python run_frontend.py

test:
	python -m pytest -q