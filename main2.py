from flask import Flask, request, redirect
import shortuuid

app = Flask(__name__)

# Dictionary to store the mapping of short URLs to long URLs
url_mapping = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = shorten_url(long_url)
        return f"Shortened URL: {short_url}"
    return """
    <form method="post">
        Long URL: <input type="text" name="long_url"><br>
        <input type="submit" value="Shorten">
    </form>
    """

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found."

def shorten_url(long_url):
    # Generate a unique short code using shortuuid
    short_code = shortuuid.uuid()[:6]  # Use the first 6 characters as the short code

    # Store the mapping between the short and long URLs
    url_mapping[short_code] = long_url

    # Create the short URL
    short_url = f"http://127.0.0.1:5000/{short_code}"  # Use this for local testing

    return short_url

if __name__ == "__main__":
    app.run()
