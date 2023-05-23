# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class CompanyData(db.Model):
    __tablename__ = 'company_data'

    company_id = db.Column(db.String(32), primary_key=True)
    company_href = db.Column(db.String(128), nullable=False)
    company_name = db.Column(db.String(64), nullable=False)
    company_type = db.Column(db.String(32))
    company_attribute = db.Column(db.String(64))
    company_size = db.Column(db.String(45))



class JobData(db.Model):
    __tablename__ = 'job_data'

    job_id = db.Column(db.String(32), primary_key=True)
    job_href = db.Column(db.String(128), nullable=False)
    company_id = db.Column(db.ForeignKey('company_data.company_id'), nullable=False, index=True)
    job_title = db.Column(db.String(256), nullable=False)
    area_id = db.Column(db.ForeignKey('work_area.area_id'), nullable=False, index=True)
    job_salary = db.Column(db.String(45))
    salary_min = db.Column(db.Float(asdecimal=True))
    salary_max = db.Column(db.Float(asdecimal=True))
    job_welf = db.Column(db.String(128))
    job_education = db.Column(db.String(64))
    job_experience = db.Column(db.String(64))
    job_update = db.Column(db.String(64))

    area = db.relationship('WorkArea', primaryjoin='JobData.area_id == WorkArea.area_id', backref='job_data')
    company = db.relationship('CompanyData', primaryjoin='JobData.company_id == CompanyData.company_id', backref='job_data')



class WorkArea(db.Model):
    __tablename__ = 'work_area'

    area_id = db.Column(db.String(32), primary_key=True, info='主键')
    area_name = db.Column(db.String(45), nullable=False, server_default=db.FetchedValue())
    parent_id = db.Column(db.String(32))
