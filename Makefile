run-main:
	@python src/main.py

set_path:
	@export PYTHONPATH='/home/ivan/Documents/Jira_analyser/'		# needs to be typed into terminal

freeze-reqs:
	@pip freeze > requirements.txt