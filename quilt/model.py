import datetime

from quilt.app import Base
from sqlalchemy import Integer, Column, String, Text, DateTime, Boolean


class KeyValue(Base):
    __tablename__ = "key_value"
    id = Column(Integer, primary_key=True)
    key = Column(String(255))
    val = Column(Text)
    date_added_utc = Column(DateTime, default=datetime.datetime.utcnow())


class BuildFlow(Base):
    __tablename__ = "build_flow"
    id = Column(Integer, primary_key=True)
    uri = Column(String(255))
    docker_repo_image = Column(String(255))

    @property
    def project_name(self):
        from quilt.action import util


        return util.project_name_from_git_uri(self.uri)


class BuildHistory(Base):
    __tablename__ = "build_history"
    id = Column(Integer, primary_key=True)
    build_flow_id = Column(Integer, primary_key=True)
    success = Column(Boolean)
    timestamp_utc = Column(DateTime)
    finished_timestamp_utc = Column(DateTime)
