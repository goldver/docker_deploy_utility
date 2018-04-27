#!/usr/bin/python3
import subprocess
import utils
import logs

logger = logs.logger
env_config = utils.get_params('env_conf.json')


# generates redis ip
def get_redis_ip(env_profile):
    if env_config[env_profile]['redis_ip'].count('.') == 3:
        logger.warn("Using full IP address configuration for cache cleaning.")
        return env_config[env_profile]['redis_ip']

    return env_config[env_profile]['env_network'] + env_config[env_profile]['redis_ip']


# clear Redis cache
def clear_cache(redis_ip):
    logger.info("Flushes on Redis IP: " + redis_ip)
    cmd = " flushall"
    redis_cli_process_cmd = "redis-cli -h " + redis_ip + cmd

    flushall_process = subprocess.Popen([redis_cli_process_cmd], shell=True, stdout=subprocess.PIPE)
    try:
        flushall_process.wait(300)
    except subprocess.TimeoutExpired:
        flushall_process.kill()
        raise Exception("Failed to clean cache. Time out on connection attempt..")

    exit_status = flushall_process.returncode
    if exit_status == 0:
        logger.info("Successfully clean cache")
    else:
        raise Exception("Failed to clean cache. Returned with failure code.")
