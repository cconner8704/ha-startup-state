#!/bin/sh

echo "Running set-ha-state.py with '$*'"
echo "Evironment:"
env
/bin/bash -l -c "$*"
