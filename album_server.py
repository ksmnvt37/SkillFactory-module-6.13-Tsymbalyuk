from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):

    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "<h3>Всего найдено {} альбомов {}: </h3>".format(len(albums_list), artist)
        result += "<p>"+"<br>".join(album_names)+"</p>"
    return result

@route("/albums", method="POST")
def new_album():

    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }

    for key, value in album_data.items():
        valid, message = validate_it(key, value)
        if not valid:
            return HTTPError(449, message)

    existing_album = album.find_album(album_data)
    if existing_album:
        return HTTPError(409, "Данный альбом уже существует в базе данных. Его id - {}.".format(existing_album.id))

    added_album = album.add_album(album_data)
    if added_album:
        print("Альбом сохранен в базу данных")
        return "Данные об альбоме успешно сохранены"

def validate_it(key, value):

    if key == "year":
        try:
            value = int(value)
        except ValueError as e:
            return False, "Год должен быть числом, а не строкой"
        else:
            if value < 1900 or value > 2020:
                return False, "Год должен быть не меньше 1900 и не больше 2020"
            else:
                return True, ""
    else:
        if len(value) == 0:
            return False, "В поле {} не введено значение".format(key)
        else:
            return True, ""

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)