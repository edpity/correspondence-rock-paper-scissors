import os
import pandas as pd
import pickle
from time import sleep
from flask import Flask, render_template, request
from waitress import serve
#from flask_socketio import SocketIO, send, emit
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__,template_folder="templates")
#app.config['SECRET_KEY'] = 'rock'
#app.config['host'] = '0.0.0.0'
#app.config['port'] = int(os.environ.get('PORT', 5001))
#app.config['debug'] = True
#socketio = SocketIO(app)

userframe = pd.read_csv('userframe.csv')

statefile = 'picklestate.pk'
with open(statefile, 'wb') as sfile:
    pickle.dump(0, sfile)

pickfile = 'picklechoice.pk'
with open(pickfile, 'wb') as pfile:
    pickle.dump(1, pfile)

counterfile = 'picklecounterchoice.pk'
with open(counterfile, 'wb') as cfile:
    pickle.dump(0, cfile)


@app.route("/", methods=['POST','GET'])
def home():

    if request.method == 'POST':
        if userframe['user'].isin([request.form['user']]).any():
            if request.form['pass'] == userframe[userframe['user'] == request.form['user']]['pass'].item():
                return render_template('play.html')
            else:
                return render_template('wrongpassword.html')
        else:
            return render_template('usernotfound.html')
    else:
        return render_template('login.html')

@app.route("/register", methods=['POST','GET'])
def register():

    if request.method == 'POST':
        if userframe['user'].isin([request.form['user']]).any():
            return render_template('useralreadyexists.html')
        else:
            if request.form['user'] == '':
                return render_template('usernamecannotbeblank.html')
            elif request.form['pass'] == '':
                return render_template('passwordcannotbeblank.html')
            else:
                userframe.loc[len(userframe)] = [request.form['user'], request.form['pass']]
                userframe.to_csv('userframe.csv', index=False)
                return render_template('login.html')
    else:
        return render_template('register.html')
    
@app.route("/play", methods=['POST'])
def play():
    
    global player
    global pick
    global counterpick
    
    with open(statefile, 'rb') as sfile:
        state = pickle.load(sfile)
       
    if state == 0:
        pick = request.form.get('data')
        counterpick = 0
        with open(statefile, 'wb') as sfile:
            pickle.dump(1, sfile)
        with open(pickfile, 'wb') as pfile:
            pickle.dump(pick, pfile)
        with open(counterfile, 'wb') as cfile:
            pickle.dump(counterpick, cfile)
        while counterpick == 0:
            sleep(2)
            with open(counterfile, 'rb') as cfile:
                counterpick = pickle.load(cfile)
        else:
            player = 1
            result = eval()
            return(result)

    elif state == 1:
        counterpick = request.form.get('data')
        with open(statefile, 'wb') as sfile:
            pickle.dump(0, sfile)
        with open(counterfile, 'wb') as cfile:
            pickle.dump(counterpick, cfile)
        with open(pickfile, 'rb') as pfile:
            pick = pickle.load(pfile)
        player = 2
        result = eval()
        return(result)

def eval():

    if pick == '1':
        choice = 'rock'
    elif pick == '2':
        choice = 'paper'
    elif pick == '3':
        choice = 'scissors'

    if counterpick == '1':
        against = 'rock'
    elif counterpick == '2':
        against = 'paper'
    elif counterpick == '3':
        against = 'scissors'  

    if (choice == 'rock' and against == 'paper'):
        status = 0
    elif (choice == 'rock' and against == 'scissors'):
        status = 2
    elif (choice == 'rock' and against == 'rock'):
        status = 1
    elif (choice == 'paper' and against == 'paper'):
        status = 1
    elif (choice == 'paper' and against == 'scissors'):
        status = 0
    elif (choice == 'paper' and against == 'rock'):
        status = 2
    elif (choice == 'scissors' and against == 'paper'):
        status = 2
    elif (choice == 'scissors' and against == 'scissors'):
        status = 1
    elif (choice == 'scissors' and against == 'rock'):
        status = 0
    else:
        status = 0


    if (status == 2 and player == 2):
        return(choice.capitalize() + ' beats ' + against + '! You lose.')
    elif (status == 1 and player == 2):
        return('Draw!')
    elif (status == 0 and player == 2):
        return(against.capitalize() + ' beats ' + choice + '! You win.')
    elif (status == 2 and player == 1):
        return(choice.capitalize() + ' beats ' + against + '! You win.')
    elif (status == 1 and player == 1):
        return('Draw!')
    elif (status == 0 and player == 1):
        return(against.capitalize() + ' beats ' + choice + '! You lose.')
    else:
        return('Error')

@app.route("/state", methods=['GET'])    
def turn():
    with open(statefile, 'rb') as sfile:
        state = pickle.load(sfile)
    return(str(state))

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 6969))
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    #socketio.run(app)
    #app = app.run(host='10.0.0.1', port=port, debug=True)
    serve(app, host='0.0.0.0', port=6969)

