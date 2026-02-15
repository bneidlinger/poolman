#!/bin/bash
# Launches Chromium in kiosk mode pointed at the Poolman dashboard.
# Waits for the Flask server to be ready before opening the browser.

POOLMAN_URL="http://localhost:5000"

# Disable screen blanking / screensaver
xset s off 2>/dev/null
xset -dpms 2>/dev/null
xset s noblank 2>/dev/null

# Wait for Flask to be ready (up to 30 seconds)
echo "Waiting for Poolman at $POOLMAN_URL ..."
for i in $(seq 1 30); do
    if curl -s -o /dev/null "$POOLMAN_URL"; then
        echo "Poolman is up."
        break
    fi
    sleep 1
done

# Launch Chromium in kiosk mode
exec chromium-browser \
    --kiosk \
    --noerrdialogs \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --disable-restore-session-state \
    "$POOLMAN_URL"
