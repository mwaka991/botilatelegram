#!/bin/bash
# Render Deployment Configuration
# This file is used by Render to build and deploy the bot

# Python version
runtime: python-3.13

# Build command - installs all dependencies
build: pip install -r requirements.txt

# Start command - runs the bot
start: python bot.py

# Health check (optional - for monitoring)
# health_check:
#   protocol: http
#   path: /health
#   port: 8080
