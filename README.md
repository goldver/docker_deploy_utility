DevOps deployment utility
========================

The purpose of this script is to generate generic Docker Image for DevOps different purposes.
Currently Docker Image includes:
 - aws cli
 - postgresql-client-9.5
 - redis-tools 
 - vim
 - zip 
 - htop
 - ctop 
 - python-pip
 - python3-pip
 - requests
 - groff-base 
 - curl
 - jfrog cli

Description
==================

This Docker image dedicated for next actions:
 - Clear CDN Caching
 - Clear Redis keys
 - Upload Resources to S3 Bucket
 - Upload OnSite to S3 Bucket
 - Debugging

|  Parameter:   | Description:             | Example:               |
| ------------- |:------------------------:|:----------------------:|
| VERSION       | Package version          | 1.0-SNAPSHOT-2         |
| ENV_PROFILE   | Data Center to deploy    | xyz                    |
| SCRIPT        | Action to Execute        | upload-onsite          |

Usage
==================

Just build Jenkins job 
with required parameters:

| Action:                            | VERSION:      | ENV_PROFILE:  | SCRIPT:           | Example:                     |
|:-----------------------------------|:-------------:|:-------------:|:-----------------:|:-----------------------------|
| Upload Resources to S3 bucket      | Mandatory     | Mandatory     | upload-resources  | 2.4.0, xyz, upload-resources |
| Upload On-Site files to S3 bucket  | Mandatory     | Mandatory     | upload-onsite     | 1.0.0-3, xyz, upload-onsite  |
| Clear Redis cache                  | Non Mandatory | Mandatory     | clear-cache       | none,xyz, clear-cache        |
| Purge CDN                          | Non Mandatory | Mandatory     | purge-cdn         | none, xyz, purge-cdn         |
| Info about docker image            | Non Mandatory | Non Mandatory | info              | none, none, info             |


Example for local running
==================
- docker container
docker run --rm -t -eENV_PROFILE=xyz -eSCRIPT=purge-cdn -eVERSION=2.4.0 virtual-docker.martifactory.io/md-devops-tools:0.1.0-126-cf47179

- python code:
cd <script location> python3 main.py 0 xyz purge-cdn

Contributing
------------
1. Fork the repository on Github
2. Create a named feature branch (like `add_component_x`)
3. Write you change
4. Write tests for your change (if applicable)
5. Run the tests, ensuring they all pass
6. Submit a Pull Request using Github

License and Authors
-------------------
Authors: Michael Vershinin

Support
-------------------
goldver@gmail.com


