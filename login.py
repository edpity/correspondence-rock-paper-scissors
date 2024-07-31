import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__,template_folder="templates")

userframe = pd.read_csv('userframe.csv')
#print(userframe)
#print(userframe['user'])

@app.route("/", methods=['POST','GET'])
def home():
    error = None
    if request.method == 'POST':
        if userframe['user'].isin([request.form['user']]).any():
            if request.form['pass'] == userframe[userframe['user'] == request.form['user']]['pass'].item():
                return render_template('homme.html')
            else:
                return render_template('wrongpassword.html')
        else:
            return render_template('usernotfound.html')
    else:
        return render_template('login.html')

@app.route("/register", methods=['POST','GET'])
def register():
    error = None
    if request.method == 'POST':
        if userframe['user'].isin([request.form['user']]).any():
            return render_template('useralreadyexists.html')
        else:
            userframe.loc[len(userframe)] = [request.form['user'], request.form['pass']]
            userframe.to_csv('userframe.csv', index=True)
            return render_template('login.html')
    else:
        return render_template('register.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='127.0.0.1', port=port, debug=True)

