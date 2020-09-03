from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#db.create_all()


class CompanyNameModel(db.Model):
    __tablename__ = 'companyname'
    __table_args__ = {'sqlite_autoincrement': True}
    idx = db.Column(db.Integer, primary_key=True)
    companyId = db.Column(db.String(2), nullable=False)
    companyName = db.Column(db.String(100), nullable=False)

    def __init__(self, companyId, name, **kwargs):
        self.companyId = companyId
        self.companyName = name

    def __repr__(self):
        return "<companyname('{self.companyId}', '{self.companyName}')>"

    def getCompanyId(name):
        results = db.session.query(CompanyNameModel.companyId).filter_by(companyName=name).all()

        if len(results) != 0:
            result = results[0]
            print (result.companyId)
            return result.companyId


class CompanyTagModel(db.Model) :
    __tablename__ = 'companytag'
    __table_args__ = {'sqlite_autoincrement': True}
    idx = db.Column(db.Integer, primary_key=True)
    companyId = db.Column(db.String(2), nullable=False)
    tagName = db.Column(db.String(100),  nullable=False)

    def __init__(self, companyId, name, **kwargs):
        self.companyId = companyId
        self.tagName = name

