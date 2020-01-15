.PHONY: all launch-test-env

all: launch-test-env

launch-test-env:
	cd vagrant && vagrant up
