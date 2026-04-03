#!/usr/bin/env bash

# Install Pulumi CLI
curl --location --silent --show-error --fail https://get.pulumi.com \
    | sudo sh -s -- --install-root /usr/local

pipx install uv

# Ensure the user's home directory is owned by the user
sudo chown --recursive "$(id --user):$(id --group)" ~
