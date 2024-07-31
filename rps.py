import os
from flask import Flask, render_template, request

app = Flask(__name__,template_folder="templates")

@app.route("/")
def hello():
    return render_template('test.html')

@app.route("/play", methods=['POST'])
def play():
    global againstnext
    result = request.form.get('data')
    
    if result == '1':
        choice = 'rock'
    elif result == '2':
        choice = 'paper'
    elif result == '3':
        choice = 'scissors'

    try:
        against = againstnext
    except NameError:
        against = 'rock'

    print(choice)
    print(against)
    
    if (choice == 'rock' and against == 'paper'):
        status = 2
    elif (choice == 'rock' and against == 'scissors'):
        status = 0
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

    if status == 0:
        result = 'lose'
    elif status == 1:
        result = 'draw'
    else:
        result = 'win'

    againstnext = choice
    print(against.capitalize() + '! You ' + result + '.')
    return(against.capitalize() + '! You ' + result + '.')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
