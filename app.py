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
def get_company_info() :
    if 'companyname' in request.args:
        return get_company_info_from_companyname(request.args.get("companyname"))

    if 'tagname' in request.args:
        return get_company_info_from_tagname(request.args.get("tagname"))

    return jsonify(
        responcemessage="fail, parameter check",
        status=200
    )

def get_company_info_from_companyname(name):
    search = "%{}%".format(name)
    print(search)

    # like  search company id, name
    results = db.session.query(CompanyNameModel.companyid).filter(CompanyNameModel.companyname.like(search)).all()
    print (results)
    if len(results) == 0:
        return jsonify(
            responcemessage="fail, not exists data",
            status=200
        )

    company_list = []
    for companyname, tagnamelist in db.session.query(
            func.group_concat(CompanyNameModel.companyname.distinct()),
            func.group_concat(CompanyTagModel.tagname.distinct())
    ).filter(
        CompanyTagModel.companyid == CompanyNameModel.companyid
    ).filter(
        CompanyNameModel.companyid.in_(db.session.query(CompanyNameModel.companyid).filter(CompanyNameModel.companyname.like(search)))
    ).group_by(
       CompanyNameModel.companyid
    ).all():
        print(companyname, tagnamelist)

        arr = {}
        subdic = {companyname: tagnamelist}
        print (subdic)
        arr = subdic
        company_list.append(arr)

    return jsonify(company_list)

def get_company_info_from_tagname(name):
    company_list = []

    for companynamelist, tagnamelist in db.session.query(
        func.group_concat(CompanyNameModel.companyname.distinct()), func.group_concat(CompanyTagModel.tagname.distinct())
    ).filter(
        CompanyTagModel.companyid == CompanyNameModel.companyid
    ).filter(
        CompanyNameModel.companyid.in_(db.session.query(CompanyTagModel.companyid).filter_by(tagname=name))
    ).group_by(
        CompanyNameModel.companyid
    ).all() :
        print (companynamelist, tagnamelist)

        arr = {}
        subdic = {companynamelist: tagnamelist}
        print (subdic)
        arr[name] = subdic
        company_list.append(arr)

    return jsonify(company_list)

@app.route("/tag/<companyname>/<tagname>", methods=["POST"])
def add_tag(companyname=None, tagname=None):

    # company id 구하기
    companyid = CompanyNameModel.getCompanyId(companyname)
    print(companyid)

    # 중복 체크
    search_tag = CompanyTagModel.query.filter_by(companyid=companyid, tagname=tagname).all()
    if len(search_tag) > 0:
        return jsonify(
            responcemessage="fail, exists data",
            status=200
        )

    tag = CompanyTagModel(companyid, tagname)
    db.session.add(tag)
    db.session.commit()
    print(tag)
    return jsonify(
        responcemessage="success",
        status=200
    )

@app.route("/tag/<companyname>/<tagname>", methods=["DELETE"])
def delete_tag(companyname=None, tagname=None):

    # company id 구하기
    companyid = CompanyNameModel.getCompanyId(companyname)

    tags = CompanyTagModel.query.filter_by(companyid=companyid, tagname=tagname).all()
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


