from flask import Flask, request, jsonify
import secrets
from datetime import datetime
import threading

app = Flask(__name__)
posts = []
post_id_counter = 1
state_lock = threading.Lock()

# Create a Post
@app.route('/post', methods=['POST'])
def create_post():
    try:
        data = request.get_json()

        if not isinstance(data, dict) or 'msg' not in data or not isinstance(data['msg'], str):
            raise ValueError("Bad request. Request body must be a JSON object with a 'msg' field of type string.")

        with state_lock:
            post_id = post_id_counter
            post_id_counter += 1

            key = secrets.token_urlsafe(32)
            timestamp = datetime.utcnow().isoformat()

            new_post = {"id": post_id, "key": key, "timestamp": timestamp, "msg": data['msg']}
            posts.append(new_post)

        return jsonify({"id": post_id, "key": key, "timestamp": timestamp})

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

        response = {
            "id": post["id"],
            "timestamp": post["timestamp"],
            "msg": post["msg"]
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

            if post["key"] != key:
                return jsonify({"error": "Forbidden. Incorrect key"}), 403

            posts.remove(post)

            # Re-generate key for future posts
            new_key = secrets.token_urlsafe(32)
            timestamp = post["timestamp"]

            new_post = {"id": post["id"], "key": new_key, "timestamp": timestamp, "msg": post["msg"]}
            posts.append(new_post)

        return jsonify({"id": post["id"], "key": new_key, "timestamp": timestamp})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
