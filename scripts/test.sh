# !/bin/sh

# Exit immediately if Newman complains
set -e

# Kill the server on exit
trap 'kill $PID' EXIT

# Start the server in the background and record the PID
./run.sh &
PID=$!

# Run Newman with the specified Postman collections and environment
echo "running tests..."
newman run ../tests/forum_multiple_posts.postman_collection.json -e ../tests/env.json # Use the environment file
newman run ../tests/forum_extension1_users_and_user_keys_tests.postman_collection.json
newman run ../tests/forum_post_read_delete.postman_collection.json -n 50 # 50 iterations
echo "tests completed"