from flask import Flask
from flaskr.myapp import app
app1=app.app
if __name__ == '__main__':
    app1.run(debug=True)
