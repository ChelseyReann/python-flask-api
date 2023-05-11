from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('playlist', user='chelseyalphonso', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db
    
class Song(BaseModel):
    title = CharField()
    artist = CharField()
    album = CharField()
    
db.connect()
# db.drop_tables([Song])
# db.create_tables([Song])

# Song(title='Seek Bromance', artist ='Avicii', album='Seek Bromance').save()
# Song(title='Wildest Dreams', artist ='Taylor Swift', album=1989).save()
# Song(title='VPN', artist ='Lil Ugly Mane', album='Volanic Bird Enemy').save()
# Song(title= "Nobody Gets Me", artist= "SZA", album= "SOS").save()

app = Flask(__name__)

@app.route('/playlist', methods=['GET', 'POST'])
@app.route('/playlist/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Song.get(Song.id == id)))
        else:
            song_list = []
            for song in Song.select():
                song_list.append(model_to_dict(song))
            return jsonify(song_list)
    
    if request.method == 'PUT':
        body = request.get_json()
        Song.update(body).where(Song.id == id).execute()
        return f'Song {id}  has been updated.'
    
    if request.method == 'POST':
        new_song = dict_to_model(Song, request.get_json())
        new_song.save()
        return jsonify({"success": True})
    
    if request.method == 'DELETE':
        Song.delete().where(Song.id == id).execute()
        return f"Song {id} has been deleted."
    
app.run(debug=True, port=9000)
    