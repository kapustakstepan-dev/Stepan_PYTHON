import json

DATE_FAIL = "data.json"


def get_films(film_id=None):
    with open(DATE_FAIL, "r", encoding="utf-8") as fp:
        films = json.load(fp)["films"]
    if film_id is not None:
        return films[film_id]
    return films


def save_films(films):
    data = {"films": films}
    with open(DATE_FAIL, "w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)


def add_film(film):
    films = get_films()
    films.append(film)
    save_films(films)


def search_films(query):
    query = query.lower()
    films = get_films()
    return [film for film in films if query in film["name"].lower()]
