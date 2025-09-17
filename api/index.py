from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check_user", methods=["POST"])
def check_user():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "No username provided"}), 400

    # Step 1: Get UserId from Roblox API
    user_lookup = requests.post(
        "https://users.roblox.com/v1/usernames/users",
        json={"usernames": [username]},
        headers={"Content-Type": "application/json"}
    ).json()

    if not user_lookup.get("data") or len(user_lookup["data"]) == 0:
        return jsonify({"found": False})

    user_id = user_lookup["data"][0]["id"]

    # Step 2: Get avatar
    avatar_res = requests.get(
        f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=true"
    ).json()

    avatar_url = avatar_res["data"][0]["imageUrl"]

    return jsonify({
        "found": True,
        "userId": user_id,
        "avatarUrl": avatar_url
    })
