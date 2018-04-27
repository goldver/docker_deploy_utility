#!/usr/bin/python3
import os
import logs

logger = logs.logger

dict_env = {
    # aws - resources uploader
    "AWS_ACCESS_KEY_ID": "zzzzz",
    "AWS_SECRET_ACCESS_KEY": "zzzzzz",

    # cdn api key
    "CDN_API_KEY": "zzzzzzzz",
}


# creates env variables
def create_env_variables():
    logger.info("Setting env variables..")
    for key in dict_env:
        os.environ[key] = dict_env[key]


# destroing env variables
def destroy_env_variables():
    logger.info("Resetting env variables..")
    for key in dict_env:
        del os.environ[key]
