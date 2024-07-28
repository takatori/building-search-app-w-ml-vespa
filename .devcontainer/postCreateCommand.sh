#!/bin/sh
# postCreateCommand.sh

echo "START Install"

sudo chown -R vscode:vscode .

poetry config virtualenvs.in-project true
poetry install

echo "SETUP Vespa"

vespa config set target http://vespa:19071
vespa status
vespa deploy vespa-config --wait 30

echo "FINISH"