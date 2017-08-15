#!/usr/bin/env sh

BASEDIR="ABSOLUTE_PATH_TO_THIS_PROJECT_FOLDER"

dns_inwx_add() {
    fulldomain=$1
    txtvalue=$2
    ${BASEDIR}/acme-inwx.py --add --domain "$fulldomain" --challenge "$txtvalue"
}

dns_inwx_rm() {
    fulldomain=$1
    ${BASEDIR}/acme-inwx.py --remove --domain "$fulldomain"
}
