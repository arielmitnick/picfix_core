from flask import Flask

from core.image_editor import ImageEditor

server = Flask(__name__)


@server.route("/")
def hello():
    return "Hello World!"


@server.route("/image_editor_call")
def image_editor_call():
    editor = ImageEditor()
    return editor.say_hi()


if __name__ == "__main__":
    server.run(host='0.0.0.0')
