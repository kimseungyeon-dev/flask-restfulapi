from flask import Flask,request, jsonify
from sqlalchemy import func
from model import db, CompanyNameModel, CompanyTagModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ksy.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "FALSE"
app.config['JSON_AS_ASCII'] = False

db.init_app(app)

@app.route("/")
def hello():
    return "new Hello Flask!"

@app.route("/company", methods=["GET"])
def get_company():
    # http://localhost:5000/company?name=an
    # http://localhost:5000/company?name=티트
    name = request.args.get("name")
    search = "%{}%".format(name)
    print(search)

    # like  search company id, name
    results = db.session.query(CompanyNameModel.companyId).filter(CompanyNameModel.companyName.like(search)).all()
    print (results)
    if len(results) == 0:
        return jsonify(
            responcemessage="fail, not exists data",
            status=200
        )

    company_list = []
    for companyName, tagnamelist in db.session.query(
            func.group_concat(CompanyNameModel.companyName.distinct()),
            func.group_concat(CompanyTagModel.tagName.distinct())
    ).filter(
        CompanyTagModel.companyId == CompanyNameModel.companyId
    ).filter(
        CompanyNameModel.companyId.in_(db.session.query(CompanyNameModel.companyId).filter(CompanyNameModel.companyName.like(search)))
    ).group_by(
       CompanyNameModel.companyId
    ).all():
        print(companyName, tagnamelist)

        arr = {}
        subdic = {companyName: tagnamelist}
        print (subdic)
        arr = subdic
        company_list.append(arr)

    return jsonify(company_list)

@app.route("/company_tag", methods=["GET"])
def get_company_from_tag():
    # http://localhost:5000/company_tag?tagname=HR2
    # http://localhost:5000/company_tag?tagname=서울
    name = request.args.get("tagname")
    company_list = []

    for companynamelist, tagnamelist in db.session.query(
        func.group_concat(CompanyNameModel.companyName.distinct()), func.group_concat(CompanyTagModel.tagName.distinct())
    ).filter(
        CompanyTagModel.companyId == CompanyNameModel.companyId
    ).filter(
        CompanyNameModel.companyId.in_(db.session.query(CompanyTagModel.companyId).filter_by(tagName=name))
    ).group_by(
        CompanyNameModel.companyId
    ).all() :
        print (companynamelist, tagnamelist)

        arr = {}
        subdic = {companynamelist: tagnamelist}
        print (subdic)
        arr[name] = subdic
        company_list.append(arr)

    return jsonify(company_list)

@app.route("/tag/<companyname>/<tagname>", methods=["POST"])
def create_tag(companyname=None, tagname=None):
    # curl -X POST http://localhost:5000/tag/티트/HR

    # company id 구하기
    companyId = CompanyNameModel.getCompanyId(companyname)
    print(companyId)

    # 중복 체크
    search_tag = CompanyTagModel.query.filter_by(companyId=companyId, tagName=tagname).all()
    if len(search_tag) > 0:
        return jsonify(
            responcemessage="fail, exists data",
            status=200
        )

    tag = CompanyTagModel(companyId, tagname)
    db.session.add(tag)
    db.session.commit()
    print(tag)
    return jsonify(
        responcemessage="success",
        status=200
    )

@app.route("/tag/<companyname>/<tagname>", methods=["DELETE"])
def delete_tag(companyname=None, tagname=None):
    # curl -X DELETE http://localhost:5000/tag/wanted/HR2

    # company id 구하기
    companyId = CompanyNameModel.getCompanyId(companyname)

    tags = CompanyTagModel.query.filter_by(companyId=companyId, tagName=tagname).all()
    if len(tags) == 0 :
        return jsonify(
            responcemessage="fail, not exists data",
            status=200
        )

    db.session.delete(tags[0])
    db.session.commit()
    return jsonify(
        responcemessage="success",
        status=200
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)


