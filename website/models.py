from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import enum


class User(db.Model, UserMixin):  # User class extends db.Model and UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)

    # relationship must be written with CAPITAL LETTER (we do not know why)


class Researcher(User):
    __mapper_args__ = {
        'polymorphic_identity': 'researcher',
    }


class Evaluator(User):
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
    db.Column(
        db.Integer, db.ForeignKey('researcher.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())


class Document(db.Model):
    document_id = db.Column(db.Integer, primary_key=True)
    file_extension = db.Column(db.String(10))
    file_name = db.Column(db.String(150))
    topic = db.Column(db.String(150))
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.project_id'))


class Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    db.Column(
        db.Integer, db.ForeignKey('evaluator.id'))
    document_id = db.Column(
        db.Integer, db.ForeignKey('document.document_id'))
    description = db.Column(db.Text())