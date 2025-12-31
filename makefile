
serve:
	. .venv/bin/activate && uvicorn src.app:app --reload

install:
	pip install --upgrade pip
	pip install -r requirements.txt