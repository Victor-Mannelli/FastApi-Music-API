#!/usr/bin/env bash

# wait-for-it.sh: wait for a service to become available
# Usage: wait-for-it.sh host:port [-s] [-t timeout] [-- command args]

set -e

TIMEOUT=15
QUIET=0
STRICT=0

while [[ $# -gt 0 ]]
do
    case "$1" in
        -h|--host)
        HOST="$2"
        shift 2
        ;;
        -p|--port)
        PORT="$2"
        shift 2
        ;;
        -s|--strict)
        STRICT=1
        shift
        ;;
        -q|--quiet)
        QUIET=1
        shift
        ;;
        -t|--timeout)
        TIMEOUT="$2"
        shift 2
        ;;
        --)
        shift
        break
        ;;
        *)
        echo "Unknown argument: $1"
        exit 1
        ;;
    esac
done

if [[ -z "$HOST" || -z "$PORT" ]]; then
    echo "Error: you need to provide a host and port to test."
    exit 1
fi

if [[ $QUIET -eq 0 ]]; then
    echo "Waiting for $HOST:$PORT..."
fi

for i in $(seq $TIMEOUT); do
    nc -z "$HOST" "$PORT" && break
    if [[ $i -eq $TIMEOUT ]]; then
        if [[ $QUIET -eq 0 ]]; then
            echo "Timeout occurred after waiting $TIMEOUT seconds for $HOST:$PORT."
        fi
        exit 1
    fi
    sleep 1
done

if [[ $STRICT -eq 1 ]]; then
    if [[ $QUIET -eq 0 ]]; then
        echo "$HOST:$PORT is available after $i seconds."
    fi
    exec "$@"
else
    if [[ $QUIET -eq 0 ]]; then
        echo "$HOST:$PORT is available after $i seconds."
    fi
    exec "$@"
fi