#!/bin/bash

# Ensure you're logged into Surge (only needed once per machine)
# surge login --email you@example.com --token your-token

# Set these values
PROJECT_DIR="website"  # or the path to your build folder
DOMAIN="curly-parcel.surge.sh"  # customize this

#rm -r website/transcriptions
#cp -r transcriptions website

# Deploy
echo "🚀 Deploying to Surge..."
npx surge $PROJECT_DIR $DOMAIN
