#!/usr/bin/python3
import os
import sys
import argparse
import utils
import config
from logs import logger, shutdown

parser = argparse.ArgumentParser(prog='main',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=100,
                                                                                     width=200))
parser.add_argument('VERSION', help='Version of package we going to deploy')
parser.add_argument('ENV_PROFILE', help='Deploy Environment identifier')
parser.add_argument('SCRIPT', help='Action we want to execute')

args = parser.parse_args()


def main():
    try:
        scripts_to_execute = args.SCRIPT.split(';')
        validate_scripts_to_execute_argument(scripts_to_execute)

        version = os.environ["VERSION"] = args.VERSION
        env_profile = os.environ["ENV_PROFILE"] = args.ENV_PROFILE
        logger.info("*** Version is: " + os.environ["VERSION"] + " ***")
        logger.info("*** Environment is: " + os.environ["ENV_PROFILE"] + " ***")

        env_config = utils.get_params('env_conf.json')

        for script in scripts_to_execute:
            if script:
                logger.info("*** Executing script: " + script + " ***")
                config.create_env_variables()

                if script == 'upload-onsite':
                    import s3

                    # Preparation
                    artifact = "onsite"
                    archive = artifact + '-' + version + '.zip'
                    artifact_rt_path = 'virtual-mvn/com/' + artifact + '/' + version + '/' + archive
                    zip_source = artifact_rt_path.split("/", 1)[1]
                    dest_bucket_name = env_config[env_profile]['bucket_name']
                    dest_sub_directory = 'resources-onsite'

                    # Execution
                    s3.rt_download(package_path=artifact_rt_path)
                    s3.unzip_resouces(zip_source=zip_source)
                    s3.upload_resources(dest_bucket_name=dest_bucket_name, dest_sub_directory=dest_sub_directory)
                    s3.delete_archive(archive='com')

                elif script == 'upload-resources':
                    import s3

                    # Preparation
                    artifact = 'service-resources'
                    archive = artifact + '-' + version + '.zip'
                    top_level_domain = env_config[env_profile]['top_level_domain']
                    artifact_rt_path = 'virtual-mvn/com/' + artifact + '/' + version + '/' + archive
                    zip_source = artifact_rt_path.split("/", 1)[1]
                    dest_bucket_name = env_config[env_profile]['bucket_name']
                    dest_sub_directory = 'resources'

                    # Execution
                    s3.rt_download(package_path=artifact_rt_path)
                    s3.unzip_resouces(zip_source=zip_source)
                    s3.fix_resources(top_level_domain=top_level_domain)
                    s3.upload_resources(dest_bucket_name=dest_bucket_name, dest_sub_directory=dest_sub_directory)
                    s3.delete_archive(archive='com')

                elif script == 'purge-cdn':
                    import fastly

                    # Preparation
                    resources_cdn_service_id = env_config[env_profile]['resources_cdn_service_id']
                    website_cdn_service_id = env_config[env_profile]['website_cdn_service_id']
                    service_id = [resources_cdn_service_id, website_cdn_service_id]

                    # Execution
                    fastly.purge_cdn(service_id=service_id)

                elif script == 'clear-cache':
                    import redis

                    # Preparation
                    redis_ip = redis.get_redis_ip(env_profile)

                    # Execution
                    redis.clear_cache(redis_ip=redis_ip)

                else:
                    logger.info("### This action doesn't exist! ###")

    except Exception as ex:
        logger.info("### oops, something is wrong :( " + str(ex) + " ###")
        sys.exit(os.EX_OSERR)
    finally:
        config.destroy_env_variables()
        shutdown()


def validate_scripts_to_execute_argument(scripts_to_execute):
    supported_scripts = ['upload-onsite',
                         'upload-resources',
                         'purge-cdn',
                         'clear-cache']
    valid = True
    for script in scripts_to_execute:
        if script not in supported_scripts:
            valid = False
            logger.error("Found unsupported script: '%s'", script)

    if not valid:
        logger.error("Aborting due to unsupported scripts(s)")
        sys.exit(os.EX_OSERR)


if __name__ == "__main__":
    main()
