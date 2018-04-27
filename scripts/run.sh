#!/bin/bash

source ~/.profile # Load aliases

function checkpoint {
    if [ -z $SCRIPT ]; then
        echo "Missing environment variable SCRIPT. Please re-run with environment variable set."
        exit 1
    fi

    if [ -z $VERSION ]; then
        echo "Missing environment variable VERSION. Please re-run with environment variable set."
        exit 1
    fi

    if [ -z $ENV_PROFILE ]; then
        echo "Missing environment variable ENV_PROFILE. Please re-run with environment variable set."
        exit 1
    fi
}

function info {
	echo "Environment: $ENV_PROFILE"
	echo "Version: $VERSION"

	echo "------------------"

	aws --version
	redis-cli --version

	env | grep ENV_PROFILE

	echo "Postgres"
	echo "Redis-cli"

	echo "Resources CDN"

	echo "------------------"

	python --version
	echo "Also installed: vim zip htop ctop python-pip groff-base curl requests"
}

function entrypoint {
	python3 main.py $VERSION $ENV_PROFILE $SCRIPT
}

case ${1-$SCRIPT} in
    'upload-resources'|'upload-onsite'|'purge-cdn'|'clear-cache') entrypoint ;;
	'info') info ;;
	'bash') bash ;;
esac

