#!/usr/bin/env sh

BASEDIR=$(dirname "$(readlink -f "$0")")

dns_inwx_add() {
    fulldomain=$1
    txtvalue=$2
    ${BASEDIR}/acme-inwx.py --add --domain "$fulldomain" --challenge "$txtvalue"
}

dns_inwx_rm() {
    fulldomain=$1
    ${BASEDIR}/acme-inwx.py --remove --domain "$fulldomain"
}
