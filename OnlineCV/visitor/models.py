# -*- coding: utf-8 -*-
"""Visitor models."""
import datetime as dt

from OnlineCV.database import Column, Model, SurrogatePK, db
from OnlineCV.extensions import cache


class Visitor(SurrogatePK, Model):
    __tablename__ = 'visitors'
    ip_address = Column(db.String(80), unique=False, nullable=False)
    user_agent = Column(db.String(100), unique=False, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, ip_address, user_agent, **kwargs):
        """Create instance."""
        db.Model.__init__(self, ip_address=ip_address, user_agent=user_agent, **kwargs)

    @cache.memoize(timeout=50)
    def __repr__(self):
        """Represent instance as a unique string."""
        return f'<Visitor(ip_address={self.ip_address}, user_agent={self.user_agent})>'
