from flask import Flask, render_template, request
import uuid
from datetime import datetime
import os
import urllib2
import mysql.connector
import json

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def doReloadQuizEntries():
    global quizEntries
    quizEntries = []
    for line in urllib2.urlopen(soundsRoot + '/quiz.txt'):
        parts = line.rstrip(os.linesep).split(' ')
        quizEntries.append({'instrument': parts[0], 'file': parts[1]})

soundsRoot='https://raw.githubusercontent.com/seffka/sounds/master'
db_user='mpc'
db_password='mpc'
db_host='127.0.0.1'
database='mpc'

app = Flask(__name__)
quizEntries = []
doReloadQuizEntries()

@app.route('/reloadQuiz')
def reloadQuiz():
    doReloadQuizEntries()
    return render_template('ok.html')

@app.route('/test')
def test():
    # return render_template('quest1.html', id='abc')
    return render_template('quest1.html', id = 'abc')

@app.route('/')
def main():
    return render_template('hi.html', soundsRoot = soundsRoot)

def addEmail(email):
    user = {}
    user['id'] = uuid.uuid4().hex
    user['email'] = email
    saveUser(user)
    return user['id']

@app.route('/next', methods=['POST'])
def next_form():
    id = request.form['id']
    entryId=int(request.form['entryId'])
    yesNo=request.form['submit']
    print id, entryId, yesNo
    answer = {
        'id':id,
        'entryId':entryId,
        'instrument':quizEntries[entryId]['instrument'],
        'file':quizEntries[entryId]['file'],
        'answer':yesNo}
    saveSoundAnswer(answer)
    entryId = getNextEntry(id)
    print 'now entryId: ', entryId
    if (entryId < len(quizEntries)):
        return regularForm('regular.html', id, entryId)
    else:
        return finalForm(id)

def regularForm(templateName, id, entryId):
    progress = '(' + str(entryId+1) + '/' + str(len(quizEntries)) + ')'
    return render_template(
        templateName,
        soundsRoot = soundsRoot,
        id=id,
        entryId=entryId,
        instrument=quizEntries[entryId]['instrument'],
        wavFile=quizEntries[entryId]['file'],
        progress = progress)


def finalForm(id):
    return render_template("quest1.html", id=id)

@app.route('/saveQuest1', methods=['POST'])
def saveQuest1():
    id = request.form['id']
    answer = {
        'age':request.form['age'],
        'gender': request.form['gender'],
        'attentively': request.form['attentively'],
        'studied': request.form['studied']
    }
    saveMetaAnswer(id, "personal", answer)
    return render_template("piano.html", id=id)

@app.route('/savePiano', methods=['POST'])
def savePiano():
    id = request.form['id']
    answer = {
        'piano':request.form['piano'],
        'pianoPractice': request.form['pianoPractice'],
        'pianoNow': request.form['pianoNow'],
        'pianoAlbum1': request.form['pianoAlbum1'],
        'pianoAlbum2': request.form['pianoAlbum2'],
        'pianoAlbum3': request.form['pianoAlbum3']
    }
    saveMetaAnswer(id, "piano", answer)
    return render_template("guitar.html", id=id)

@app.route('/saveGuitar', methods=['POST'])
def saveGuitar():
    id = request.form['id']
    answer = {
        'guitar':request.form['guitar'],
        'guitarPractice': request.form['guitarPractice'],
        'guitarNow': request.form['guitarNow'],
        'guitarAlbum1': request.form['guitarAlbum1'],
        'guitarAlbum2': request.form['guitarAlbum2'],
        'guitarAlbum3': request.form['guitarAlbum3']
    }
    saveMetaAnswer(id, "guitar", answer)
    return render_template("tambura.html", id=id)

@app.route('/saveTambura', methods=['POST'])
def saveTambura():
    id = request.form['id']
    answer = {
        'tambura':request.form['tambura'],
        'tamburaPractice': request.form['tamburaPractice'],
        'tamburaNow': request.form['tamburaNow'],
        'tamburaAlbum1': request.form['tamburaAlbum1'],
        'tamburaAlbum2': request.form['tamburaAlbum2'],
        'tamburaAlbum3': request.form['tamburaAlbum3']
    }
    saveMetaAnswer(id, "tambura", answer)
    return render_template("harpsichord.html", id=id)

@app.route('/saveHarpsichord', methods=['POST'])
def saveHarpsichord():
    id = request.form['id']
    answer = {
        'harpsichord':request.form['harpsichord'],
        'harpsichordPractice': request.form['harpsichordPractice'],
        'harpsichordNow': request.form['harpsichordNow'],
        'harpsichordAlbum1': request.form['harpsichordAlbum1'],
        'harpsichordAlbum2': request.form['harpsichordAlbum2'],
        'harpsichordAlbum3': request.form['harpsichordAlbum3']
    }
    saveMetaAnswer(id, "harpsichord", answer)
    return render_template("final.html", id=id)

@app.route('/saveFinal', methods=['POST'])
def saveFinal():
    id = request.form['id']
    answer = {
        'suggestions': request.form['suggestions']
    }
    saveMetaAnswer(id, "suggestions", answer)
    return render_template("thanks.html", id=id)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    email = request.form['inputEmail']
    id = addEmail(email)
    return regularForm('sample.html', id, 0)

# DB
def saveUser(record):
    cnx = mysql.connector.connect(user=db_user, password=db_password,
                                  host=db_host,
                                  database=database)
    cursor = cnx.cursor()
    add_employee = ("INSERT INTO usr "
                    "(id, email, logtime) "
                    "VALUES (%s, %s, %s)")
    data_employee = (record['id'], record['email'], datetime.now().isoformat())
    cursor.execute(add_employee, data_employee)
    cnx.commit()
    cursor.close()
    cnx.close()

def saveSoundAnswer(record):
    cnx = mysql.connector.connect(user=db_user, password=db_password,
                                  host=db_host,
                                  database=database)
    cursor = cnx.cursor()
    add_q = ("INSERT INTO SOUNDS "
                    "(usr_id, snd_id, instrument, file, answer, logtime) "
                    "VALUES (%s, %s, %s, %s, %s, %s)")
    data_q = (record['id'], record['entryId'], record['instrument'],
                     record['file'], record['answer'], datetime.now().isoformat())
    cursor.execute(add_q, data_q)
    cnx.commit()
    cursor.close()
    cnx.close()

def saveMetaAnswer(id, meta_id, map):
    cnx = mysql.connector.connect(user=db_user, password=db_password,
                                  host=db_host,
                                  database=database)
    cursor = cnx.cursor()
    add_q = ("INSERT INTO META "
                    "(usr_id, META_ID, answer, logtime) "
                    "VALUES (%s, %s, %s, %s)")
    data_q = (id, meta_id, json.dumps(map), datetime.now().isoformat())
    cursor.execute(add_q, data_q)
    cnx.commit()
    cursor.close()
    cnx.close()

def getNextEntry(id):
    cnx = mysql.connector.connect(user=db_user, password=db_password,
                                  host=db_host,
                                  database=database)
    cursor = cnx.cursor()
    query = "SELECT MAX(SND_ID) FROM SOUNDS WHERE USR_ID = '" + id + "'"

    cursor.execute(query)
    row = cursor.fetchone()
    if (row[0] is None):
        return 0
    else:
        return row[0] + 1

if __name__ == '__main__':
    app.run()
