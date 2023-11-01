from io import BytesIO
from flask import Flask, request, session
from flask import jsonify
from flask import render_template, redirect, flash
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from PIL import Image
import io
import base64
import hashlib
from uuid import uuid4

# Importing module
import mysql.connector
 
app = Flask(__name__)
app.debug = True

app.secret_key = "secret key"

# Creating connection object
mydb = mysql.connector.connect(
  host = "asuapretni.mysql.pythonanywhere-services.com",
  user = "asuapretni",
  password = "_M1y2sql",
  database='asuapretni$final_db'
)
 
# Printing the connection object
print(mydb)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

cursor = mydb.cursor()
bcrypt = Bcrypt(app)
CORS(app)

# Show database
cursor.execute("SHOW TABLES")
 
for x in cursor:
  print(x)


# Formulario
@app.route('/form')
def form_render():
  cursor = mydb.cursor()
  cursor = mydb.cursor(dictionary=True)

  cursor.execute("SELECT * FROM pintxo p JOIN contestants c ON p.pintxo_id = c.contestants_id")
  pintxo_all = cursor.fetchall()

  return render_template('form.html', pintxo_all=pintxo_all)


# Formulario
@app.route('/form', methods=["POST"])
def form_data():
  _pintxo_name = request.form['pintxo_name']
  _pintxo_description = request.form['pintxo_description']
  _pintxo_img = request.files['pintxo_img']
  

  _contestants_name = request.form['contestants_name']
  _contestants_address = request.form['contestants_address']
  _contestants_cp = request.form['contestants_cp']
  _contestants_town = request.form['contestants_town']

  cursor = mydb.cursor()
  cursor = mydb.cursor(dictionary=True)
  
  pintxo_img2 = base64.b64encode(_pintxo_img.read())
  pintxo_img = repr(pintxo_img2)[2:-1]

  insert_pintxo = "INSERT INTO PINTXO(pintxo_name, pintxo_description, pintxo_img)" "VALUES(%s, %s, %s)"
  insert_contestant = "INSERT INTO CONTESTANTS(contestants_name, contestants_address, contestants_cp, contestants_town)" "VALUES(%s, %s, %s, %s)"
  insert_votes = "INSERT INTO votes(votes_number)" "VALUES (0)"

  new_pintxo = (_pintxo_name, _pintxo_description, pintxo_img)
  new_contestant = (_contestants_name, _contestants_address, _contestants_cp, _contestants_town)

  disable = "SET FOREIGN_KEY_CHECKS=0"
  enable = "SET FOREIGN_KEY_CHECKS=1"
  cursor.execute(disable)
  cursor.execute(insert_pintxo, new_pintxo)
  cursor.execute(insert_contestant, new_contestant)
  cursor.execute(insert_votes)
  cursor.execute(enable)

  mydb.commit()

  flash("Information added sucessfully!")

  return redirect('/form')

  cursor.close() 
  mydb.close()

# Formulario Delete_form pintxos
@app.route('/delete/<id>')
def delete_pintxo_form(id):
  cursor = mydb.cursor()
  cursor = mydb.cursor(dictionary=True)

  delete_pintxo = ("DELETE FROM pintxo WHERE pintxo_id="+id)
  delete_contestant = ("DELETE FROM contestants WHERE contestants_id="+id)

  cursor.execute(delete_pintxo)
  cursor.execute(delete_contestant)

  mydb.commit()
  response = jsonify('Info succesfully deleted')
  print(response)

  flash("Information deleted sucessfully!")

  return redirect('/form')

  cursor.close() 
  mydb.close()


# Formulario update_form pintxos
@app.route('/update/<id>', methods=["POST", "GET"])
def update_pintxo_form(id):
  cursor = mydb.cursor()
  cursor = mydb.cursor(dictionary=True)
  
  cursor.execute("SELECT * FROM pintxo p JOIN contestants c ON p.pintxo_id = c.contestants_id WHERE p.pintxo_id="+id)
  pintxo_all = cursor.fetchone()

  print(pintxo_all)

  if request.method == "POST":
    pintxo_name = request.form['pintxo_name']
    pintxo_description = request.form['pintxo_description']
    pintxo_img = request.files['pintxo_img']
  
    contestants_name = request.form['contestants_name']
    contestants_address = request.form['contestants_address']
    contestants_cp = request.form['contestants_cp']
    contestants_town = request.form['contestants_town']

    pintxo_img2 = base64.b64encode(pintxo_img.read())
    pintxo_img = repr(pintxo_img2)[2:-1]

    update_pintxo = "UPDATE PINTXO SET pintxo_name=%s, pintxo_description=%s, pintxo_img=%s WHERE pintxo_id="+id
    update_contestant = "UPDATE CONTESTANTS SET contestants_name=%s, contestants_address=%s, contestants_cp=%s, contestants_town=%s WHERE contestants_id="+id
  
    new_pintxo = (pintxo_name, pintxo_description, pintxo_img)
    new_contestant = (contestants_name, contestants_address, contestants_cp, contestants_town)

    disable = "SET FOREIGN_KEY_CHECKS=0"
    enable = "SET FOREIGN_KEY_CHECKS=1"
    cursor.execute(disable)
    cursor.execute(update_pintxo, new_pintxo)
    cursor.execute(update_contestant, new_contestant)
    cursor.execute(enable)

    mydb.commit()
    
    flash("Information updated sucessfully!")
   
    return redirect('/form')
   
  return render_template('update.html', pintxo_all=pintxo_all)

  cursor.close() 
  mydb.close()


# Endpoint to create a new pintxo
@app.route('/pintxo', methods=["POST"])
def add_pintxo():
    _pintxo_name = request.json['pintxo_name']
    _pintxo_description = request.json['pintxo_description']

    cursor = mydb.cursor()
    cursor = mydb.cursor(dictionary=True)

    insert_pintxo = "INSERT INTO PINTXO(pintxo_name, pintxo_description)" "VALUES(%s, %s)"

    new_pintxo = (_pintxo_name, _pintxo_description)
    cursor.execute(insert_pintxo, new_pintxo)
    mydb.commit()
    response = jsonify('Pintxo succesfully added')
    print(response)
    return redirect('/form')

    cursor.close() 
    mydb.close()  

# Endpoint to get pintxos
@app.route('/pintxos', methods=["GET"])
def get_pintxo():
    cursor = mydb.cursor()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pintxo")
    pintxo_all = cursor.fetchall()
    response = jsonify(pintxo_all)
    return response

    cursor.close() 
    mydb.close()
  

  # Endpoint to get pintxos
@app.route('/pintxos_votes', methods=["GET"])
def get_pintxo_votes():
    cursor = mydb.cursor()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pintxo p JOIN votes v ON p.pintxo_id = v.votes_id")
    pintxo_votes = cursor.fetchall()
    response = jsonify(pintxo_votes)
    return response

    cursor.close() 
    mydb.close()

# Endpoint to Update pintxos
@app.route('/update')
def update_pintxo():

    return 'update'


# Endpoint to delete pintxos
@app.route('/delete/<id>', methods=["DELETE"])
def delete_pintxo(id):
  cursor = mydb.cursor()
  cursor = mydb.cursor(dictionary=True)

  delete_pintxo = ("DELETE FROM pintxo WHERE pintxo_id="+id)
  delete_vote = ("DELETE FROM votes WHERE votes_id="+id)

  cursor.execute(delete_pintxo)
  cursor.execute(delete_vote)
  mydb.commit()
  response = jsonify('Pintxo succesfully deleted')
  return response
  
  cursor.close() 
  mydb.close()


# Endpoint to votes POST
@app.route('/votes', methods=["POST"])
def add_votes():
    _votes_id = request.json['votes_id']
    _votes_number = request.json['votes_number']

    cursor = mydb.cursor()
    cursor = mydb.cursor(dictionary=True)

    insert_vote = "INSERT INTO votes(votes_id, votes_number)" "VALUES(%s, %s)"

    new_vote = (_votes_id, _votes_number)
    cursor.execute(insert_vote, new_vote)
    mydb.commit()
    response = jsonify('vote succesfully added')
    print(response)
    return response

    cursor.close() 
    mydb.close()  

# Endpoint to votes PATCH
@app.route('/votes', methods=["PATCH"])
def add_more_votes():
    _votes_id = request.json['votes_id']
    _votes_number = request.json['votes_number']

    cursor = mydb.cursor()
    cursor = mydb.cursor(dictionary=True)

    update_vote = "UPDATE votes SET votes_number=%s WHERE votes_id =%s"

    new_vote = (_votes_number, _votes_id)
    cursor.execute(update_vote, new_vote)
    mydb.commit()
    response = jsonify('vote succesfully added')

    print(response)
    return response
  
    cursor.close()
    mydb.close()  

# Endpoint to votes get_id
@app.route('/votes/<id>', methods=["GET"])
def get_votes_id(id):
  cursor = mydb.cursor()
  cursor = mydb.cursor(dictionary=True)

  get_vote_id = ("SELECT votes_number FROM votes WHERE votes_id="+id)

  cursor.execute(get_vote_id)
  votes_numbers = cursor.fetchone()
  response = jsonify(votes_numbers)
  return response
  
  cursor.close() 
  mydb.close()
  
if __name__ == '__main__':
  app.run(debug=True)