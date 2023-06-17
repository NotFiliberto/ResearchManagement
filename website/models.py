from sqlalchemy.dialects.postgresql import UUID
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import uuid
import enum


class User(db.Model, UserMixin):  # User class extends db.Model and UserMixin
    user_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)

    # relationship must be written with CAPITAL LETTER (we do not know why)
    researcher = db.relationship('Researcher')
    evaluator = db.relationship('Evaluator')


class Researcher(db.Model):
    user_id = db.Column(db.String(150), db.ForeignKey('user.user_id'))


class Evaluator(db.Model):
    user_id = db.Column(db.String(150), db.ForeignKey('user.user_id'))


class Evaluation_Interval(db.Model):
    evaluation_interval_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start = db.Column(db.Date())
    end = db.Column(db.Date())


class ProjectStatus(enum.Enum):
    APPROVED = 'approved'
    SUBMITTED_FOR_EVALUATION = 'submitted_for_evaluation'
    REQUIRES_CHANGES = 'requires_changes'
    NOT_APPROVED = 'not_approved'


class Project(db.Model):
    project_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = db.Column(
        db.Enum(ProjectStatus, values_callable=lambda obj: [
                e.value for e in obj]),
        nullable=False,
        default=ProjectStatus.NOT_APPROVED.value,
        server_default=ProjectStatus.NOT_APPROVED.value
    )
    evaluation_interval_id = db.Column(db.String(150), db.ForeignKey(
        'evaluation_interval.evaluation_interval_id'))
    researcher_id = db.Column(
        db.String(150), db.ForeignKey('researcher.user_id'))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())


class Document(db.Model):
    document_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_extension = db.Column(db.String(10))
    file_name = db.Column(db.String(150))
    topic = db.Column(db.String(150))
    project_id = db.Column(db.String(150), db.ForeignKey(
        'project.project_id'))


class Report(db.Model):
    report_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluator_id = db.Column(
        db.String(150), db.ForeignKey('evaluator.user_id'))
    document_id = db.Column(
        db.String(150), db.ForeignKey('document.document_id'))
    description = db.Column(db.Text())


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # foreign keys must be LOWER CASE
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
