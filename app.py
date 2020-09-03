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
        responsemessage="fail, parameter check",
        status=200
    )

def get_company_info_from_companyname(name):
    # http://localhost:5000/company?companyname=an
    # http://localhost:5000/company?companyname=티트
    search = "%{}%".format(name)

    # like  search company id, name
    results = db.session.query(CompanyNameModel.companyid).filter(CompanyNameModel.companyname.like(search)).all()
    if len(results) == 0:
        return jsonify(
            responsemessage="fail, not exists data",
            status=200
        )

    company_list = []
    for companyid, companynamelist, tagnamelist in db.session.query(
            CompanyNameModel.companyid,
            func.group_concat(CompanyNameModel.companyname.distinct()),
            func.group_concat(CompanyTagModel.tagname.distinct())
    ).filter(
        CompanyTagModel.companyid == CompanyNameModel.companyid
    ).filter(
        CompanyNameModel.companyid.in_(db.session.query(CompanyNameModel.companyid).filter(CompanyNameModel.companyname.like(search)))
    ).group_by(
       CompanyNameModel.companyid
    ).all():
        arr = {}
        arr_sub = {}
        arr_sub["company"] = companynamelist
        arr_sub["tag"] = tagnamelist.replace(',','|')
        arr[companyid] = arr_sub
        company_list.append(arr)

    return jsonify(company_list)

def get_company_info_from_tagname(name):
    # http://localhost:5000/company?tagname=HR2
    # http://localhost:5000/company?tagname=서울
    company_list = []

    for companyid, companynamelist, tagnamelist in db.session.query(
        CompanyNameModel.companyid, func.group_concat(CompanyNameModel.companyname.distinct()), func.group_concat(CompanyTagModel.tagname.distinct())
    ).filter(
        CompanyTagModel.companyid == CompanyNameModel.companyid
    ).filter(
        CompanyNameModel.companyid.in_(db.session.query(CompanyTagModel.companyid).filter_by(tagname=name))
    ).group_by(
        CompanyNameModel.companyid
    ).all() :
        arr = {}
        arr_sub = {}
        arr_sub["company"] = companynamelist
        arr_sub["tag"] = tagnamelist.replace(',','|')
        arr[companyid] = arr_sub
        company_list.append(arr)

    return jsonify(company_list)

@app.route("/tag/<companyname>/<tagname>", methods=["POST"])
def add_tag(companyname=None, tagname=None):
    # curl -X POST http://localhost:5000/tag/티트/HR

    # company id 구하기
    companyid = CompanyNameModel.getCompanyId(companyname)

    # 중복 체크
    search_tag = CompanyTagModel.query.filter_by(companyid=companyid, tagname=tagname).all()
    if len(search_tag) > 0:
        return jsonify(
            responsemessage="fail, exists data",
            status=200
        )

    tag = CompanyTagModel(companyid, tagname)
    db.session.add(tag)
    db.session.commit()
    return jsonify(
        responsemessage="success",
        status=200
    )

@app.route("/tag/<companyname>/<tagname>", methods=["DELETE"])
def delete_tag(companyname=None, tagname=None):
    # curl -X DELETE http://localhost:5000/tag/wanted/HR2

    # company id 구하기
    companyid = CompanyNameModel.getCompanyId(companyname)

    tags = CompanyTagModel.query.filter_by(companyid=companyid, tagname=tagname).all()
    if len(tags) == 0 :
        return jsonify(
            responsemessage="fail, not exists data",
            status=200
        )

    db.session.delete(tags[0])
    db.session.commit()
    return jsonify(
        responsemessage="success",
        status=200
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)


