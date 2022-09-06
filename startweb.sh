#!/bin/bash

sleep 5
chromium-browser http://localhost:8000 \
  --check-for-update-interval=31536000 \
  --start-fullscreen \
  --kiosk \
  --noerrdialogs \
  --disable-translate \
  --no-first-run \
  --no-context-menu \
  --disable-context-menu \
  --fast \
  --fast-start \
  --disable-infobars \
  --overscroll-history-navigation=0 \
  --disable-pinch \
  --disable-session-crashed-bubble \
  --disable-sync \
  --disable-features=TouchpadOverscrollHistoryNavigation
