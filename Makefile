all: build callouts

build:
	./build.sh

callouts:
	python replace_callouts.py

clean:
	rm -rf website/*
