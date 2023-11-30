import pandas as pd
import sqlite3

moviesDB = pd.read_csv('moviesDB.csv') 

connection = sqlite3.connect('moviesDB.db') 
with open('schema.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

for index, movie in moviesDB.iterrows():
    try:
        cursor.execute('INSERT INTO moviesDB (ReleaseYear, Title, Origin, Director, Genre, Wikipedia, Resume) VALUES (?,?,?,?,?,?,?)',
                       (movie['ReleaseYear'], movie['Title'], movie['Origin'], movie['Director'], movie['Genre'], movie['Wikipedia'], movie['Resume']))
    except sqlite3.IntegrityError as e:
        print(f"Erreur lors de l'insertion de la ligne {index + 1}: {e}")
        print(movie)

connection.commit()
connection.close()
