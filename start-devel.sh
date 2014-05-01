#!/bin/bash
#
# Run this script to start a local development server.
# First you must fill you github application credentials below.
#

export GITHUB_CLIENT_ID=${1:-61cb47b917c4a38ec20c}
export GITHUB_CLIENT_SECRET=${2:-d88ca6a0c8199b4fe0a159db7adf6a654407fd64}
export OO_INDEX_GITHUB_USERNAME=${3:-openshift}
export OO_INDEX_GITHUB_REPONAME=${4:-oo-index}
export OO_INDEX_QUICKSTART_JSON=${5:-wsgi/static/quickstart.json}
export DEBUG=${DEBUG:-1}

if [ -z "$GITHUB_CLIENT_ID" -o -z "$GITHUB_CLIENT_SECRET" ]; then
	echo "Usage: $0 GITHUB_CLIENT_ID GITHUB_CLIENT_SECRET [OO_INDEX_GITHUB_USERNAME [OO_INDEX_GITHUB_REPONAME [OO_INDEX_QUICKSTART_JSON]]]"
	exit 1
fi

set -e

[ -d virtenv ] || virtualenv --no-site-packages virtenv
. virtenv/bin/activate
egrep -o '[a-zA-Z0-9-]+==[0-9.]+' setup.py | xargs pip install

python wsgi/myflaskapp.py
