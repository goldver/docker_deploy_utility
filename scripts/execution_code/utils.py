#!/usr/bin/python3
import os
import logs
import requests

logger = logs.logger
devops_bucket = 'zzz'
url = 'https://s3.eu-central-1.amazonaws.com/' + devops_bucket + '/configuration/'
files = ['env_conf.json', 'service_conf.json']


# get configurations params
def get_params(file):
    try:
        response = requests.get(url + file).json()
        env_list = dict()
        for item in response.keys():
            env_list[item] = response.get(item)
        return env_list
    except Exception as ex:
        logger.info("### Can't find any configuration file following this URL.." + str(ex) + " ###")
        sys.exit(os.EX_OSERR)


# raise exeption in os system
def os_system(command):
    value = os.system(command)
    if value != 0:
        raise Exception("System func execption")
