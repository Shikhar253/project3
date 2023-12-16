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
newman run ./forum_multiple_posts.postman_collection.json -e ./env.json # Use the environment file
newman run ./forum_post_read_delete.postman_collection.json -n 50 # 50 iterations
newman run ./forum_extension1_users_and_user_keys_tests.postman_collection.json
newman run ./orum_extension2_user_profile_tests.postman_collection.json
newman run ./forum_extension3_4_5_tests.postman_collection.json

echo "tests completed"