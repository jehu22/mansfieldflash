from flask import Flask, send_from_directory
import os

# Create the Flask app
app = Flask(__name__, static_folder="static")

# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------
@app.route("/")
def home():
    """
    Serve the pre-generated static HTML page.
    The page is generated once a day by generate_static_news.py.
    """
    return send_from_directory("public", "index.html")

# Optional: 404 page
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 - Page Not Found</h1>", 404

# ---------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Use the port assigned by Render, default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
