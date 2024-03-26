setup:
	python3 -m venv env
active-env:
	source env/bin/activate
push:
	rsync -av --no-perms --no-owner --no-group --delete --filter=':- .gitignore' .  sirasit@10.40.29.189:/home/sirasit/agent