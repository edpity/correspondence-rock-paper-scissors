import os
import pandas as pd
import pickle
from flask import Flask, render_template, request

app = Flask(__name__,template_folder="templates")

userframe = pd.read_csv('userframe.csv')
statefile = 'picklestate.pk'
with open(statefile, 'wb') as sfile:
    pickle.dump(0, sfile)

choicefile = 'picklechoice.pk'
with open(choicefile, 'wb') as cfile:
    pickle.dump(1, cfile)


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
            userframe.loc[len(userframe)] = [request.form['user'], request.form['pass']]
            userframe.to_csv('userframe.csv', index=True)
            return render_template('login.html')
    else:
        return render_template('register.html')
    
@app.route("/play", methods=['POST'])
def play():
    with open(statefile, 'rb') as sfile:
        state = pickle.load(sfile)
       
    if state == 0:
        pick = request.form.get('data')
        with open(statefile, 'wb') as sfile:
            pickle.dump(1, sfile)
        with open(choicefile, 'wb') as cfile:
            pickle.dump(pick, cfile)
        return('')
    
    elif state == 1:
        counterpick = request.form.get('data')
        with open(statefile, 'wb') as sfile:
            pickle.dump(0, sfile)
        with open(choicefile, 'rb') as cfile:
            pick = pickle.load(cfile)
     
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

    if status == 2:
        return(choice.capitalize() + ' beats ' + against + '! You lose.')
    elif status == 1:
        return('Draw!')
    else:
        return(against.capitalize() + ' beats ' + choice + '! You win.')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)

