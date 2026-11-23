from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    JSON,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.common import UUIDPrimaryKeyMixin, TimestampMixin


class LogEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "logs"

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "environment_id"],
            ["environments.organization_id", "environments.id"],
            name="fk_log_environment_tenant",
        ),
        ForeignKeyConstraint(
            ["organization_id", "service_id"],
            ["services.organization_id", "services.id"],
            name="fk_log_service_tenant",
        ),
        CheckConstraint(
            "level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')",
            name="valid_log_level",
        ),
        Index("ix_logs_org_recorded_at", "organization_id", "recorded_at"),
        Index("ix_logs_service_recorded_at", "service_id", "recorded_at"),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    environment_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    service_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    level: Mapped[str] = mapped_column(String(10), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    attributes: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict
    )


class MetricPoint(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "metrics"

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "environment_id"],
            ["environments.organization_id", "environments.id"],
            name="fk_metric_environment_tenant",
        ),
        ForeignKeyConstraint(
            ["organization_id", "service_id"],
            ["services.organization_id", "services.id"],
            name="fk_metric_service_tenant",
        ),
        Index("ix_metrics_org_recorded_at", "organization_id", "recorded_at"),
        Index(
            "ix_metrics_service_name_time",
            "service_id", "metric_name", "recorded_at"
        ),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    environment_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    service_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(150), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(30))
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    labels: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict
    )


class TraceSpan(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "traces"

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "environment_id"],
            ["environments.organization_id", "environments.id"],
            name="fk_trace_environment_tenant",
        ),
        ForeignKeyConstraint(
            ["organization_id", "service_id"],
            ["services.organization_id", "services.id"],
            name="fk_trace_service_tenant",
        ),
        UniqueConstraint(
            "organization_id", "service_id", "trace_id", "span_id",
            name="uq_trace_span_identity"
        ),
        Index("ix_traces_trace_id", "trace_id"),
        Index("ix_traces_service_start", "service_id", "started_at"),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    environment_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    service_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    trace_id: Mapped[str] = mapped_column(String(64), nullable=False)
    span_id: Mapped[str] = mapped_column(String(32), nullable=False)
    parent_span_id: Mapped[str | None] = mapped_column(String(32))
    operation_name: Mapped[str] = mapped_column(String(200), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="UNSET", server_default="UNSET"
    )
    attributes: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict
    )


class ServiceDependency(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "service_dependencies"

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "source_service_id"],
            ["services.organization_id", "services.id"],
            ondelete="CASCADE",
            name="fk_dependency_source_tenant",
        ),
        ForeignKeyConstraint(
            ["organization_id", "target_service_id"],
            ["services.organization_id", "services.id"],
            ondelete="CASCADE",
            name="fk_dependency_target_tenant",
        ),
        UniqueConstraint(
            "organization_id", "source_service_id", "target_service_id",
            name="uq_service_dependency"
        ),
        CheckConstraint(
            "source_service_id <> target_service_id",
            name="no_self_dependency"
        ),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    source_service_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    target_service_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    dependency_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="calls", server_default="calls"
    )
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )