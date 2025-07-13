#!/bin/bash
# Simple one-click deployment script for DeerFlow
set -e
uv sync
if [ ! -f conf.yaml ]; then
  cp conf.yaml.example conf.yaml
fi
./bootstrap.sh -d
