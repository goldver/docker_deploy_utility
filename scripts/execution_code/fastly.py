#!/usr/bin/python3
import subprocess
import os
import utils
import logs

logger = logs.logger
env_config = utils.get_params('env_conf.json')


# purge cdn
def purge_cdn(service_id):
    try:
        for service in service_id:
            logger.info("Purging CDN for service: " + service)

            cmd = "curl -s -X POST -H Fastly-Key:" + os.environ[
                "CDN_API_KEY"] + " https://api.fastly.com/service/" + service + "/purge_all"
            output_bytes = subprocess.check_output([cmd], shell=True)
            if output_bytes.decode('utf8') == '{"status":"ok"}':
                logger.info('\033[92mCDN purged for %s service\033[0m' % service)
            else:
                raise Exception('### Check Service ID or Api Key.. ###')
    except subprocess.CalledProcessError as e:
        output_bytes = e.output
        code = e.returncode

        logger.info('\033[93mCDN purge is failed for %s service. Response: %s Error code: %s\033[0m' % service,
                    output_bytes.decode('utf8'), code)

        logger.error("Failed to purge CDN for '%s' service. Response: '%s' Error code: '%s'",
                     service.name,
                     output_bytes.decode('utf8'),
                     code)

        raise Exception("Failed to purge CDN")
