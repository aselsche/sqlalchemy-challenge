## Step 2 - Climate App
# 1. import Flask
from flask import Flask


# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# Use Flask to create your routes.


# 2. Create an app, being sure to pass __name__
app = Flask(__climate__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"


# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


if __name__ == "__main__":
    app.run(debug=True)
