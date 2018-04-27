# /bin/env python
import os
import shutil
import utils
import subprocess
import logs

logger = logs.logger
env_config = utils.get_params('env_conf.json')


# get artifact
def rt_download(package_path):
    logger.info("Downloading artifact from: " + package_path)

    rt_process = subprocess.Popen(['jfrog', 'rt', 'dl', package_path], stdout=subprocess.PIPE)
    try:
        rt_process.wait(300)
    except subprocess.TimeoutExpired:
        rt_process.kill()
        raise Exception("Get Artifact is failed! Time out on connection attempt..")

    exit_status = rt_process.returncode
    if exit_status != 0:
        raise Exception("Get Artifact is failed! Returned with failure code..")


# unzips files
def unzip_resouces(zip_source):
    destination = 'resources/'
    logger.info("Unzipping archive '%s' into '%s'", zip_source, destination)
    exit_status = os.system("unzip " + zip_source + " -d " + destination)
    if exit_status == 0:
        logger.info("Archive unzipped successfully")
    else:
        raise Exception("Archive unzipping was failed!")


# upload resources to s3
def upload_resources(dest_bucket_name, dest_sub_directory):
    source = 'resources/'
    logger.info("Uploading to bucket '%s' under subdirectory: '%s'", dest_bucket_name, dest_sub_directory)

    exit_status = os.system(
        "AWS_ACCESS_KEY_ID=" + os.environ["AWS_ACCESS_KEY_ID"] + "\
         AWS_SECRET_ACCESS_KEY=" + os.environ["AWS_SECRET_ACCESS_KEY"] + "\
         aws s3 sync ./" + source + " s3://" + dest_bucket_name + "/" + dest_sub_directory)
    logger.info("The files were uploaded to bucket: " + dest_bucket_name)
    if exit_status != 0:
        raise Exception("Upload resources was failed!")


# fix resources for upload-resources script
def fix_resources(top_level_domain):
    logger.info("*** Top level domain: " + top_level_domain + " ***")

    exit_status = os.system("./fix-resources.sh " + top_level_domain)
    logger.info("Updated environment details in the resources files..")
    if exit_status != 0:
        raise Exception("Failed to update environment details in the resources files")


# delete archives
def delete_archive(archive):
    logger.info("Cleaning directories after execution..")

    for dir in [archive, 'resources']:
        shutil.rmtree(dir)
