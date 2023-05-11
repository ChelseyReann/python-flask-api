from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('playlist', user='chelseyalphonso', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db
    
class Playlist(BaseModel):
    title = CharField()
    artist = CharField()
    album = CharField()
    
db.connect()
db.drop_tables([Playlist])
db.create_tables([Playlist])

Playlist(title='Seek Bromance', artist ='Avicii', album='Seek Bromance').save()
Playlist(title='Wildest Dreams', artist ='Taylor Swift', album=1989).save()
Playlist(title='VPN', artist ='Lil Ugly Mane', album='Volanic Bird Enemy').save()

app = Flask(__name__)

@app.route('/playlist', methods=['GET', 'POST'])
@app.route('/playlist/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Playlist.get(Playlist.id == id)))
        else:
            playlist_list = []
            for playlist in Playlist.select():
                playlist_list.append(model_to_dict(playlist))
            return jsonify(playlist_list)
    
    if request.method == 'PUT':
        body = request.get_json()
        Playlist.update(body).where(Playlist.id == id).execute()
        return 'Playlist ' +str(id) + ' has been updated.'
    
    if request.method == 'POST':
        new_song = dict_to_model(Playlist, request.get_json())
        new_song.save()
        return jsonify({"success": True})
    
    if request.method == 'DELETE':
        Playlist.delete().where(Playlist.id == id).execute()
        return 'Playlist ' + str(id) + " deleted."
    
app.run(debug=True, port=9000)
    