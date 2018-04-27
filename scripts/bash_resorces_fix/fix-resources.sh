#!/bin/bash

# Assumes we built the UI using env=xyz-cloud and that the script is executed from within the ROOT folder.
# Usage: fix-resources.sh $ENV_PROFILE
TOP_LEVEL_DOMAIN=$1
echo "Setting top level domain to: ${TOP_LEVEL_DOMAIN}"
grep -RF "===MD-ENV-INDEPENDENT-TOKEN===" resources/* | cut -d':' -f1 | sort -u | xargs -n 1 -I GENERATED_FILE ./fix-single-resource.sh "https://resources.${ENV_PROFILE}.xyz.${TOP_LEVEL_DOMAIN}/" GENERATED_FILE
