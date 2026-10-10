#!/bin/bash
# Separate exact lists for the PVE host and container; no secrets are printed.
set -euo pipefail
case "$(hostname)" in
fh6-collector)
    rm -f -- /tmp/fh6-server-state-ready.tar /tmp/fh6-server-patch-ready.tar /tmp/fh6-server-final.tar
    # Validated, unique import directory created only by deploy.sh.
    test "$(readlink -f /tmp/fh6-import)" = /tmp/fh6-import
    rm -rf -- /tmp/fh6-import
    ;;
n100)
    rm -f -- /tmp/fh6-server-state-ready.tar /tmp/fh6-server-source.tar /tmp/fh6-server-patch-latest.tar /tmp/fh6-server-patch-ready.tar /tmp/fh6-server-final.tar
    ;;
*) echo 'Unexpected host; no cleanup' >&2; exit 1 ;;
esac
