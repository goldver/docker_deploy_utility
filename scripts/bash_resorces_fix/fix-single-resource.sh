#!/bin/bash

echo Set $2 to work with $1
sed "s|===MD-ENV-INDEPENDENT-TOKEN===|$1|g" $2 > $2.dc
mv -f $2.dc $2
