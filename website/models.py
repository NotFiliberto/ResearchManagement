from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class User(db.Model, UserMixin):  # User class extends db.Model and UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    type = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type'
    }
    # relationship must be written with CAPITAL LETTER (we do not know why)


class Researcher(User):
    __tablename__ = "researcher"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'researcher',
    }


class Evaluator(User):
    __tablename__ = "evaluator"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'evaluator',
    }


class Evaluation_Interval(db.Model):
    __tablename__ = 'evaluation_interval'
    evaluation_interval_id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Date())
    end = db.Column(db.Date())


class ProjectStatus(enum.Enum):
    APPROVED = 'approved'
    SUBMITTED_FOR_EVALUATION = 'submitted_for_evaluation'
    REQUIRES_CHANGES = 'requires_changes'
    NOT_APPROVED = 'not_approved'


class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(500))
    status = db.Column(
        db.Enum(ProjectStatus, values_callable=lambda obj: [
                e.value for e in obj]),
        nullable=False,
        default=ProjectStatus.NOT_APPROVED.value,
        server_default=ProjectStatus.NOT_APPROVED.value
    )
    evaluation_interval_id = db.Column(db.String(150), db.ForeignKey(
        'evaluation_interval.evaluation_interval_id'))

    # relations
    researcher_id = db.Column(
        db.Integer, db.ForeignKey('researcher.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())


class Document(db.Model):
    document_id = db.Column(db.Integer, primary_key=True)
    file_extension = db.Column(db.String(10))
    file_name = db.Column(db.String(150))
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.project_id'))


class Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    db.Column(
        db.Integer, db.ForeignKey('evaluator.id'))
    document_id = db.Column(
        db.Integer, db.ForeignKey('document.document_id'))
    description = db.Column(db.Text())
