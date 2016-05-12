#!/bin/bash
# regen_client.sh
# 
# Automatically regenerate the vwadaptor client using the latest 
#
# WARNING!!! Will automatically merge updates to the current branch! 
# If this is a Bad Thing, make sure to create a new, non-master branch 
# before running this.
# 
# Usage:
#
#  git checkout -b update-client && ./regen_client.sh


# first checkout a branch to merge updates to README
original_br_name=$(git branch | grep "*" | sed 's/\* //')
tmp_br_name=tmp-$(uuid)
git checkout -b $tmp_br_name

# save the current README.md which will get overwritten by swagger codegen
mv README.md README.md.bk

# XXX eventually will not be swagger branch but master
swagger-codegen generate -i https://github.com/VirtualWatershed/vwadaptor/raw/swagger/swagger.yaml -l python

# not interested in using the autogen'd git tool
rm git_push.sh

# only add swagger generated 
git add -f setup.py swagger_client

# move temporary README
tmp_readme=README-$tmp_br_name.md
mv README.md $tmp_readme

mv README.md.bk README.md

git commit -m"regenerated in temporary branch $tmp_br_name"

git checkout $original_br_name

git merge $tmp_br_name

git br -d $tmp_br_name

echo "\n\n******* Client regeneration complete! *******\n\nCreated an auto-generated README: $tmp_readme.\nInspect it to see if there's anything you want to keep then merge it manually"
