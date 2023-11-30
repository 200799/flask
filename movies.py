import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

#fonction de formatage des résultats en dictionnaire

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


#établir la connexion à la base de données
def get_db_connection():
    connection = sqlite3.connect('moviesDB.db')  
    connection.row_factory = dict_factory
    return connection

#page d'accueil

@app.route("/")
def landing_page_api():
    return "Movies API avec une base de données"


#Obtenir tous les films depuis la base de données
@app.route("/movies/all", methods=['GET'])
def get_all_movies():
    connection = get_db_connection()
    cursor = connection.cursor()
    movies = cursor.execute("SELECT * FROM moviesDB").fetchall()
    connection.close()
    return jsonify(movies)


#Obtenir un film par son ID depuis la base de données
@app.route("/movies/movie/<int:id>", methods=['GET'])
def get_movie_by_id(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    movie = cursor.execute("SELECT * FROM moviesDB where id = ?", (id,)).fetchone()
    connection.close()
    return jsonify(movie)

# Obtenir les films par genre depuis la base de données
@app.route("/movies/genre/<string:genre>", methods=['GET'])
def get_movies_by_genre(genre):
    connection = get_db_connection()
    cursor = connection.cursor()
    movies = cursor.execute("SELECT * FROM moviesDB WHERE Genre = ?", (genre,)).fetchall()
    connection.close()
    return jsonify(movies)

#Obtenir les films d'une année de réalisation depuis la base de données
@app.route("/movies/all/<int:ReleaseYear>", methods=['GET'])
def get_movie_by_releaseyear(ReleaseYear):
    connection = get_db_connection()
    cursor = connection.cursor()
    movie = cursor.execute("SELECT * FROM moviesDB where ReleaseYear = ?", (ReleaseYear,)).fetchone()
    connection.close()
    return jsonify(movie)

# Ajouter un film à la base de données
@app.route("/movies/add/movie", methods=['POST'])
def add_movie_db():
    movie = request.json
    if all(key in movie for key in ('ReleaseYear', 'Title', 'Origin', 'Director', 'Genre', 'Wikipedia', 'Resume')):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO moviesDB (ReleaseYear, Title, Origin, Director, Genre, Wikipedia, Resume) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (movie['ReleaseYear'], movie['Title'], movie['Origin'], movie['Director'], movie['Genre'], movie['Wikipedia'], movie['Resume']))
        id = cursor.lastrowid
        connection.commit()
        connection.close()
        return jsonify({'Success': f'Film ajouté avec succès, ID : {id}'}), 201
    return jsonify({'Error': 'Film doit avoir les attributs suivants: ReleaseYear, Title, Origin, Director, Genre, Wikipedia, Resume'}), 400

# Mettre à jour un film par son ID dans la base de données
@app.route("/movies/update/movie/<int:id>", methods=['PUT'])
def update_movie_by_id(id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    if ('Title' in data):
        cursor.execute('UPDATE moviesDB SET Title = ? WHERE id = ?', (data['Title'], id))
    if ('Origin' in data):
        cursor.execute('UPDATE moviesDB SET Origin = ? WHERE id = ?', (data['Origin'], id))
    if ('Director' in data):
        cursor.execute('UPDATE moviesDB SET Director = ? WHERE id = ?', (data['Director'], id))
    if ('Genre' in data):
        cursor.execute('UPDATE moviesDB SET Genre = ? WHERE id = ?', (data['Genre'], id))
    if ('Wikipedia' in data):
        cursor.execute('UPDATE moviesDB SET Wikipedia = ? WHERE id = ?', (data['Wikipedia'], id))
    if ('Resume' in data):
        cursor.execute('UPDATE moviesDB SET Resume = ? WHERE id = ?', (data['Resume'], id))
    connection.commit()
    connection.close()
    return jsonify({'Success': f'Film numéro {id} est mis à jour avec succès'}), 200

# Supprimer un film par son ID de la base de données
@app.route("/movies/delete/movie/<int:id>", methods=['DELETE'])
def delete_movie_by_id(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM moviesDB WHERE id = ?", (id,))
    connection.commit()
    connection.close()
    return jsonify({'Success': f'Film numéro {id} a été supprimé avec succès'}), 200

# Supprimer tous les films d'un genre spécifique de la base de données
@app.route("/movies/delete/genre/<string:genre>", methods=['DELETE'])
def delete_movies_by_genre(genre):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM moviesDB WHERE Genre = ?", (genre,))
    connection.commit()
    connection.close()
    return jsonify({'Success': f'Tous les films du genre {genre} ont été supprimés avec succès'}), 200

if __name__ == "__main__":
    app.run(debug=True)