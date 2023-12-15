from flask import Flask, request, jsonify
import secrets
from datetime import datetime
import threading
import logging

app = Flask(__name__)
posts = []
users = {}
user_metadata = {}
post_id_counter = 1
user_id_counter = 1
state_lock = threading.Lock()

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO) 

# Create a User
@app.route('/user', methods=['POST'])
def create_user():
    global user_id_counter, user_metadata
    try:
        data = request.get_json()
        username = data.get('username')
        real_name = data.get('real_name')
        avatar_icon = data.get('avatar_icon')

        if not username:
            raise ValueError("Username is required")

        # Check if username is unique
        if any(u_meta.get('username') == username for u_meta in user_metadata.values()):
            raise ValueError("Username already exists")

        with state_lock:
            user_id = user_id_counter
            user_id_counter += 1

            user_key = secrets.token_urlsafe(32)
            users[user_id] = user_key
            user_metadata[user_id] = {'username': username, 'real_name': real_name, 'avatar_icon': avatar_icon}

        return jsonify({"user_id": user_id, "user_key": user_key})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Get User Metadata
@app.route('/user/<user_identifier>', methods=['GET'])
def get_user_metadata(user_identifier):
    try:
        # Check if the identifier is a digit and thus a user ID
        if user_identifier.isdigit():
            user_id = int(user_identifier)
            user_data = user_metadata.get(user_id)
            if user_data:
                return jsonify(user_data)
            else:
                return jsonify({"error": "User not found"}), 404
        else:
            # Search by username
            for uid, metadata in user_metadata.items():
                if metadata.get('username') == user_identifier:
                    return jsonify(metadata)

            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Edit User Metadata
@app.route('/user/<string:key>', methods=['PUT'])
def edit_user_metadata(key):
    try:
        # Find user ID by key
        user_id = None
        for uid, ukey in users.items():
            if ukey == key:
                user_id = uid
                break

        if user_id is None:
            return jsonify({"error": "Invalid key"}), 403

        data = request.get_json()
        with state_lock:
            user_data = user_metadata.get(user_id, {})
            user_data.update(data)
            user_metadata[user_id] = user_data

        return jsonify({"message": "User metadata updated"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Create a Post
@app.route('/post', methods=['POST'])
def create_post():
    global post_id_counter
    try:
        data = request.get_json()


        if not isinstance(data, dict) or 'msg' not in data or not isinstance(data['msg'], str):
            return jsonify({'err': 'Bad request. Request body must be a JSON object with a "msg" field of type string'}), 400
        
        user_id =data.get('user_id')
        user_key = data.get('user_key')
        if user_id:
            user_id=int(user_id)
        # app.logger.info("user id: %s", user_id)
        # app.logger.info("user id is int? %s", isinstance(user_id,int))
        # app.logger.info("user id not in users?",user_id not in users)
        # app.logger.info("users[user_id] != user_key?",users[user_id] != user_key)
        # app.logger.info("user key: %s", user_key)
        username = 'Unknown'

        # Check if both or none of the user_id and user_key are provided
        if (user_id is None) != (user_key is None):  # XOR logic
            return jsonify({'error': 'Both user_id and user_key must be provided or neither'}), 400

        # Validate user only if user_id and user_key are provided
        if user_id is not None and user_key is not None:
            if not isinstance(user_id, int) or user_id not in users or users[user_id] != user_key:
                return jsonify({'error': 'Invalid user id or key'}), 403
            username = user_metadata.get(user_id, {}).get('username', 'Unknown')

        with state_lock:
            post_id = post_id_counter
            post_id_counter += 1

            key = secrets.token_urlsafe(32)
            timestamp = datetime.utcnow().isoformat()

            new_post = {"id": post_id, "key": key, "timestamp": timestamp, "msg": data['msg'], "user_id": user_id, "user_key": user_key, "username": username}
            posts.append(new_post)

        return jsonify({"id": post_id, "key": key, "timestamp": timestamp, "user_id": user_id, "user_key": user_key, "username": username})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Read a Post
@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    try:
        with state_lock:
            post = next((p for p in posts if p["id"] == post_id), None)

        if not post:
            return jsonify({"error": f"Post with id {post_id} not found"}), 404
        user_id = post.get("user_id")
        username = user_metadata.get(user_id, {}).get('username', 'Unknown')

        response = {
            "id": post["id"],
            "timestamp": post["timestamp"],
            "msg": post["msg"],
            "user_id": post.get("user_id"),
            "user_key": post.get("user_key"),
            "username": username
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a Post
@app.route('/post/<int:post_id>/delete/<string:key>', methods=['DELETE'])
def delete_post(post_id, key):
    try:
        with state_lock:
            post = next((p for p in posts if p["id"] == post_id), None)

            if not post:
                return jsonify({"error": f"Post with id {post_id} not found"}), 404

            if key != post["key"] and (not post.get("user_id") or key != users.get(post["user_id"])):
                return jsonify({"error": "Forbidden. Incorrect key"}), 403

            posts.remove(post)

        user_id = post.get("user_id")
        username = user_metadata.get(user_id, {}).get('username', 'Unknown')

        return jsonify({"id": post["id"], "key": post["key"], "timestamp": post["timestamp"], "user_id": user_id, "user_key": post.get("user_key"),
                        "username": username}),200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Search for posts within a date/time range
@app.route('/posts', methods=['GET'])
def search_posts():
    start = request.args.get('start')
    end = request.args.get('end')

    try:
        # Convert start and end times to datetime objects
        if start:
            start = datetime.fromisoformat(start)
        if end:
            end = datetime.fromisoformat(end)

        filtered_posts = []
        with state_lock:
            for post in posts:
                post_time = datetime.fromisoformat(post['timestamp'])
                if (not start or post_time >= start) and (not end or post_time <= end):
                    filtered_posts.append(post)

        return jsonify(filtered_posts)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Search for posts by a specific user
@app.route('/posts/user/<int:user_id>', methods=['GET'])
def search_posts_by_user(user_id):
    try:
        with state_lock:
            user_posts = [post for post in posts if post.get('user_id') == user_id]

        if not user_posts:
            return jsonify({"error": "Invalid user ID"}), 400

        return jsonify(user_posts)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Full-text search on the contents of the post's message
@app.route('/posts/search', methods=['GET'])
def search_posts_by_content():
    query = request.args.get('query', '')

    try:
        with state_lock:
            matching_posts = [post for post in posts if query.lower() in post['msg'].lower()]

        return jsonify(matching_posts)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
