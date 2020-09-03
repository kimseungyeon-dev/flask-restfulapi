from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#db.create_all()


class CompanyNameModel(db.Model):
    __tablename__ = 'companyname'
    __table_args__ = {'sqlite_autoincrement': True}
    idx = db.Column(db.Integer, primary_key=True)
    companyid = db.Column(db.String(2), nullable=False)
    companyname = db.Column(db.String(100), nullable=False)

    def __init__(self, companyid, name, **kwargs):
        self.companyid = companyid
        self.companyname = name

    def __repr__(self):
        return "<companyname('{self.companyid}', '{self.companyname}')>"

    def getCompanyId(name):
        results = db.session.query(CompanyNameModel.companyid).filter_by(companyname=name).all()

        if len(results) != 0:
            result = results[0]
            print (result.companyid)
            return result.companyid


class CompanyTagModel(db.Model) :
    __tablename__ = 'companytag'
    __table_args__ = {'sqlite_autoincrement': True}
    idx = db.Column(db.Integer, primary_key=True)
    companyid = db.Column(db.String(2), nullable=False)
    tagname = db.Column(db.String(100),  nullable=False)

    def __init__(self, companyid, name, **kwargs):
        self.companyid = companyid
        self.tagname = name

