start:
	uvicorn main:app --reload --host 0.0.0.0 --port 9999

save-dep:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt -v

kill-port-mac:
	netstat -vanp tcp | grep 3000