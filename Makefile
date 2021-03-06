all: lib run

run:
	dev_appserver.py .

lib:
	pip install -r requirements.txt -t lib/

test:
	python test.py ~/google-cloud-sdk/platform/google_appengine/ ./tests/

deploy:
	gcloud app deploy

clean:
	$(RM) -rf *~ *.pyc lib
	$(RM) -rf $(shell find . -name *~)
	find . -name "*.pyc" -exec $(RM) -f {} \;
