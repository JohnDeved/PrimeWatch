#!/bin/bash

# Fetch the GitHub secret contents
GH_SECRET=$(gh secret list | grep CONFIG_INI | awk '{print $1}')

# Write the secret contents to config.ini
echo "$GH_SECRET" > config.ini
