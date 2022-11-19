#!/bin/bash
set -e
cd /logviewer2

yarn_current_md5=$(md5sum /logviewer2/yarn.lock | cut -d ' ' -f 1)
if [ ! -f "/version/yarn_lock" ]; then
    echo "yarn version lock not found, running installer again and writing version hash"
    yarn install --frozen-lockfile
    echo "$yarn_current_md5" > /version/yarn_lock
fi
yarn_pre_md5=$(</version/yarn_lock)

if [ "$yarn_current_md5" != "$yarn_pre_md5" ]; then
    echo "MD5 do not match for yarn, updating to current lockfile"
    yarn install --frozen-lockfile
    echo "$yarn_current_md5" > /version/yarn_lock
fi

poetry_current_md5=$(md5sum /logviewer2/poetry.lock | cut -d ' ' -f 1)
if [ ! -f "/version/poetry_lock" ]; then
    echo "poetry version lock not found, running installer again and writing version hash"
    poetry install
    echo "$poetry_current_md5" > /version/poetry_lock
fi
poetry_pre_md5=$(</version/poetry_lock)

if [ "$poetry_current_md5" != "$poetry_pre_md5" ]; then
    echo "MD5 do not match for poetry, updating to current lockfile"
    poetry install
    echo "$poetry_current_md5" > /version/poetry_lock
fi




exec "$@"