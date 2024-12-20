#!/bin/bash

# Read the contents of config.ini
CONFIG_CONTENT=$(cat config.ini)

# Update the GitHub secret with the contents of config.ini
gh secret set CONFIG_INI -b"$CONFIG_CONTENT"
