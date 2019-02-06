from flask import Flask, request, jsonify
from flask_restful import Api
from pymongo import MongoClient
from bson.objectid import ObjectId

# Flask-RESTful stuff
app = Flask(__name__)
api = Api(app)

# PyMongo stuff
client = MongoClient('localhost', 27017)
banco = client['test-database']
colecao = banco['test-collection']


@app.route('/buy/', methods=['POST'])
def buy():
    i = 0
    queryarray = {"vmsreturned": []}

    try:
        data = request.json
    except:
        data = None

    if data:
        qtd_cpu = data["specs"]["cpu"]
        qtd_ram = data["specs"]["ram"]
        qtd_dsk = data["specs"]["dsk"]

        cursor = colecao.find({"vm_specs.using": 0, "vm_specs.qtd_cpu": qtd_cpu, "vm_specs.qtd_ram": qtd_ram, "vm_specs.qtd_dsk": qtd_dsk})\
                        .sort("vm_specs.price", 1)

        if not cursor.count():
            return jsonify(error="Não existem MVs com estas especificações", success=False)

        while i < data["qtd_vms"]:
            foundvm = next(cursor, None)

            if foundvm:
                colecao.update_one({"_id": foundvm["_id"]}, {"$set": {"vm_specs.using": 1}})

                jsonquery = colecao.find_one({"_id": foundvm["_id"]}, {"_id": 0})
                id = colecao.find_one({"_id": foundvm["_id"]}).get("_id")
                objid = {"objectid": str(id)}
                jsonquery.update(objid)

                queryarray["vmsreturned"].append(jsonquery)
            else:
                return jsonify(data=queryarray, msg="Existem apenas "+str(i)+" MVs com a especificação requisitada", success=True)

            i+=1

        return jsonify(data=queryarray, success=True)
    else:
        return jsonify(error="O JSON passado está corrompido, ou não foi passado um JSON via POST.", success=False)


@app.route('/add/', methods=['POST'])
def add():
    try:
        data = request.json
    except:
        data = None

    if data:
        x = colecao.insert_one(data).inserted_id
        return jsonify(vm_id=str(x), success=True)
    else:
        return jsonify(error="O JSON passado está corrompido, ou não foi passado um JSON via POST.", success=False)


@app.route('/release/', methods=['POST'])
def release():
    try:
        data = request.json
    except:
        data = None

    if data:
        colecao.update_one({"_id": ObjectId(data["objid"])}, {"$set": {"vm_specs.using" : 0}})
        return jsonify(success=True)
    else:
        return jsonify(error="O JSON passado está corrompido, ou não foi passado um JSON via POST.", success=False)


if __name__ == '__main__':
    app.run(debug=True)
