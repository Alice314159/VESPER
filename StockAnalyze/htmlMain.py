from flask import Flask
app = Flask('flaskTest')

@app.route('/')
def hello_world():
    return 'hello world'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
