#!/bin/sh

# This script will run the Streamlit application and log any errors.

# Create a log file to capture output
LOGFILE=/tmp/app.log
touch $LOGFILE

echo "--- Starting application, logging to $LOGFILE ---"

# Run the streamlit application in the background and pipe its output to the log file.
# The '2>&1' part ensures that both standard output and standard error are captured.
streamlit run main_app.py --server.port=8080 --server.address=0.0.0.0 > $LOGFILE 2>&1 &

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
