import logging
import os
from fuzzywuzzy import process
from openai import OpenAI
import csv
import pickle
from scipy.spatial.distance import cosine
import numpy as np
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
from usearch.index import Index

ndim = 1536
index = Index(ndim=ndim, metric='cos')

client = OpenAI(
        api_key="put_your_api_key_here",
        organization="put_your_organization_id_here"
    )


def generate_embeddings(tv_shows, model="text-embedding-ada-002"):
    embeddings = {}
    for title, (genre, description) in tv_shows.items():
        combined_input = f"{genre}. {description}"
        response = client.embeddings.create(input=[combined_input], model=model).data[0].embedding

        logging.info(f"Embedding for {title} dimension: {len(response)}")
        if len(response) == ndim:
            embedding_array = np.array(response)
            embeddings[title] = embedding_array
            index.add(title, embedding_array)
        else:
            logging.warning(f"Embedding for {title} has incorrect dimension")
    return embeddings


def load_or_generate_embeddings():
    embeddings_file = 'tv_show_embeddings.pkl'
    if os.path.exists(embeddings_file):

        with open(embeddings_file, 'rb') as f:
            return pickle.load(f)

    else:
        logging.info("***generateing file in the first time***")
        tv_shows = {}
        with open('imdb_tvshows.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tv_shows[row['Title']] = (row['Genres'], row['Description'])

        embeddings = generate_embeddings(tv_shows)
        for title, embedding in embeddings.items():
            index.add(title, np.array(embedding))

        with open(embeddings_file, 'wb') as f:
            pickle.dump(embeddings, f)
        return embeddings
            

def cosine_similarity(vec_a, vec_b):
    return 1 - cosine(vec_a, vec_b)


def get_recommendations(favorite_shows, embeddings, index, tv_shows_list):
    if len(favorite_shows) <= 1:
        return []

    favorite_show_vectors = [embeddings[show] for show in favorite_shows if show in embeddings]

    if not favorite_show_vectors:
        return []

    average_vector = np.mean(favorite_show_vectors, axis=0)

    if average_vector.shape[0] != ndim:
        logging.error(f"Average vector dimension ({average_vector.shape[0]}) does not match index dimension ({ndim})")
        return []

    matches = index.search(average_vector, 5)

    recommended_shows = [tv_shows_list[match.key] for match in matches]
    formatted_recommendations = []
    for show, match in zip(recommended_shows, matches):
        similarity = 1 - match.distance
        percentage = round(similarity * 100, 2)
        formatted_recommendations.append(f"{show} ({percentage}%)")

    return formatted_recommendations


def generate_fictional_show(shows, model="gpt-3.5-turbo"):
    prompt = f'''Create a name and description for a TV show that fans of {', '.join(shows)} would enjoy. 
    Format the response as follows:
    Name: [name of the show in max 2 words]
    Description: [show description in max 10 words, make sure is different from the name of the show]'''

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content.strip()

    parts = text.split('\n')
    if len(parts) >= 2:
        name_part = parts[0].split(': ', 1)
        desc_part = parts[1].split(': ', 1)
        name = name_part[1].strip() if len(name_part) > 1 else "Name not available"
        description = desc_part[1].strip() if len(desc_part) > 1 else "Description not available"
        return name, description
    else:
        return "Name not available", "Description not available"


def generate_image_with_dalle(description, model="dall-e-3"):
    prompt = f"Generate an image representing a TV show about: {description}"

    image_response = client.images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,    
    )

    image_data = image_response.data[0].url
    return image_data


def display_image(image_data):
    response = requests.get(image_data)
    image = Image.open(BytesIO(response.content))
    plt.imshow(image)
    plt.axis('off')
    plt.show()


logging.basicConfig(level=logging.INFO, format='%(message)s')

tv_shows_list = []

with open('imdb_tvshows.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        tv_shows_list.append(row[0])


def suggest_closest_matches(user_input, tv_shows_list):
    favorite_shows = [show.strip() for show in user_input.split(',')]
    closest_matches = set()

    for show in favorite_shows:
        if show:
            matches = process.extract(show, tv_shows_list, limit=1)
            for match, score in matches:
                if score >= 80:
                    closest_matches.add(match)

    return sorted(list(closest_matches))


def show_suggester(user_input, tv_shows_list):
    closest_matches = suggest_closest_matches(user_input, tv_shows_list)

    if len(closest_matches) == 0:
        logging.warning("No close matches found for the entered TV shows.")
        return []

    return closest_matches


def interactive_show_suggester():
    while True:
        logging.info("Which TV shows did you love watching? Separate them by a comma.\nMake sure to enter more than 1 show")
        user_input = input()
        closest_matches = show_suggester(user_input, tv_shows_list)

        if not closest_matches:
            continue

        logging.info(f"Just to make sure, do you mean {', '.join(closest_matches)}? (y/n)")
        user_response = input().lower()
        if user_response == 'y' and len(closest_matches) > 1:
            logging.info("Great! Generating recommendations…")
            recommendations = get_recommendations(closest_matches, load_or_generate_embeddings(),index, tv_shows_list)
            formatted_recommendations = "".join(recommendations)
            logging.info(f"Here are the TV shows that I think you would love:{formatted_recommendations}\n")

            show1name, show1description = generate_fictional_show(user_input)
            image1 = generate_image_with_dalle(show1description)

            show2name, show2description = generate_fictional_show(user_input)
            image2 = generate_image_with_dalle(show2description)

            display_image(image1)
            display_image(image2)

            logging.info(f'''I have also created just for you two shows which I think you would love.
                Show #1 is based on the fact that you loved the input shows that you
                gave me. Its name is {show1name} and it is about {show1description}.
                Show #2 is based on the shows that I recommended for you. Its name is
                {show2name} and it is about {show2description}.
                Here are also the 2 tv show ads. Hope you like them!''')

            return
         
        else:
            logging.info("Sorry about that. Let's try again, please make sure to write the names of the TV shows correctly")


if __name__ == "__main__":
    interactive_show_suggester()
