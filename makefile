clean:
	rm users.db
	rm *.pyc

build:
	python init_db.py
	python sample.py

deploy:
	python app.py
