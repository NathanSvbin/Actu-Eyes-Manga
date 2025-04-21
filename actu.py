from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from urllib.parse import urljoin

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Adala-News en ligne 🎉"

@app.route("/api/actus")
def get_actus():
    articles_needed = 50
    base_url = "https://adala-news.fr"
    category_url = base_url + "/category/anime/page/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    result = []
    current_page = 1

    while len(result) < articles_needed:
        # Construire l'URL avec la page actuelle
        url = category_url + str(current_page) + "/"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": f"Erreur {response.status_code} sur la page {current_page}."})

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')

        for article in articles:
            h2 = article.find('h2')
            a_tag = article.find('a')

            if h2 and a_tag:
                title = h2.get_text(strip=True)
                link = a_tag['href']

                img_tag = article.find('a', class_='penci-image-holder')
                image = ""
                if img_tag:
                    img_url = img_tag.get('data-bgset') or ""
                    if not img_url:
                        style = img_tag.get('style', "")
                        if 'background-image' in style:
                            img_url = style.split('url("')[1].split('")')[0]
                    image = urljoin(base_url, img_url) if img_url else ""

                result.append({
                    "titre": title,
                    "lien": link,
                    "image": image
                })

                if len(result) >= articles_needed:
                    break

        current_page += 1

    return jsonify(result[:articles_needed])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
