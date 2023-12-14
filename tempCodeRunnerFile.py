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