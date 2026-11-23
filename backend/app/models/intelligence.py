from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    JSON,
    UniqueConstraint,
    Float,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.common import UUIDPrimaryKeyMixin, TimestampMixin


class Anomaly(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "anomalies"

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "environment_id"],
            ["environments.organization_id", "environments.id"],
            name="fk_anomaly_environment_tenant",
        ),
        ForeignKeyConstraint(
            ["organization_id", "service_id"],
            ["services.organization_id", "services.id"],
            name="fk_anomaly_service_tenant",
        ),
        CheckConstraint(
            "severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')",
            name="valid_anomaly_severity"
        ),
        CheckConstraint(
            "status IN ('OPEN', 'ACKNOWLEDGED', 'RESOLVED')",
            name="valid_anomaly_status"
        ),
        CheckConstraint(
            "score >= 0 AND score <= 1",
            name="valid_anomaly_score"
        ),
        Index("ix_anomalies_org_detected", "organization_id", "detected_at"),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    environment_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    service_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    anomaly_type: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="OPEN", server_default="OPEN"
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    details: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class Incident(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "incidents"

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "environment_id"],
            ["environments.organization_id", "environments.id"],
            name="fk_incident_environment_tenant",
        ),
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_incident_org_id",
        ),
        CheckConstraint(
            "severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')",
            name="valid_incident_severity"
        ),
        CheckConstraint(
            "status IN ('OPEN', 'INVESTIGATING', 'RESOLVED', 'CLOSED')",
            name="valid_incident_status"
        ),
        Index("ix_incidents_org_status", "organization_id", "status"),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    environment_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="OPEN", server_default="OPEN"
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Evidence(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "evidence"

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "incident_id"],
            ["incidents.organization_id", "incidents.id"],
            ondelete="CASCADE",
            name="fk_evidence_incident_tenant",
        ),
        Index("ix_evidence_incident_time", "incident_id", "observed_at"),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    incident_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    source_type: Mapped[str] = mapped_column(String(30), nullable=False)
    source_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True))
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class RootCauseCandidate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "root_cause_candidates"

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "incident_id"],
            ["incidents.organization_id", "incidents.id"],
            ondelete="CASCADE",
            name="fk_root_cause_incident_tenant",
        ),
        ForeignKeyConstraint(
            ["organization_id", "service_id"],
            ["services.organization_id", "services.id"],
            name="fk_root_cause_service_tenant",
        ),
        CheckConstraint(
            "confidence_score >= 0 AND confidence_score <= 1",
            name="valid_root_cause_confidence"
        ),
        CheckConstraint("rank > 0", name="valid_root_cause_rank"),
        Index("ix_root_causes_incident_rank", "incident_id", "rank"),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    incident_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    service_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    rank: Mapped[int] = mapped_column(nullable=False)
    evidence_ids: Mapped[list] = mapped_column(
        JSON, nullable=False, default=list
    )