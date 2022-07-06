from flask import Flask
from flask import request
from flask_cors import CORS
from src.logic.ItemListGenerator import ItemListGenerator
from src.logic.ItemTypeGetter import ItemTypeGetter
from src.logic.ItemSearch import ItemSearch


app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/listItem")
def getListItem():

    offset = request.args.get('offset')
    filterWord = request.args.get('filterWord')
    return ItemListGenerator().generate(offset, filterWord)


@app.route("/searchItem")
def searchItem():

    keyword = request.args.get('keyword')
    return ItemSearch().search(keyword)


@app.route("/type")
def getType():

    return ItemTypeGetter().get()
