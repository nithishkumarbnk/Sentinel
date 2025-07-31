#!/bin/sh

# This script will run the Streamlit application and log any errors.

# Create a log file to capture output
LOGFILE=/tmp/app.log
touch $LOGFILE

echo "--- Starting application with full path, logging to $LOGFILE ---"

# --- THE DEFINITIVE FIX ---
# We are now calling streamlit using its full, absolute path.
# This bypasses any issues with the system's PATH variable.
/root/.local/bin/streamlit run main_app.py --server.port=8080 --server.address=0.0.0.0 > $LOGFILE 2>&1 &

# Wait a few seconds to give the app time to start or crash
sleep 15

# Check if the streamlit process is still running
if ! pgrep -f "streamlit run"; then
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo "!!!               APPLICATION FAILED TO START                !!!"
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo "--- Displaying the last 50 lines of the log file ---"
  tail -n 50 $LOGFILE
  # Exit with an error code to make sure the Render deploy fails visibly
  exit 1
else
  echo "--- Application started successfully ---"
  echo "--- Tailing logs (use Render's log stream to view) ---"
  # Keep the script running and tail the log file so we can see live output
  tail -f $LOGFILE
fi
