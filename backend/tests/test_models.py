from app.database.base import Base
from app.models import (
    Organization,
    User,
    Membership,
    Environment,
    Service,
    APIKey,
    LogEvent,
    MetricPoint,
    TraceSpan,
    ServiceDependency,
    Anomaly,
    Incident,
    Evidence,
    RootCauseCandidate,
)


def test_all_core_models_are_registered():
    expected_tables = {
        "organizations",
        "users",
        "memberships",
        "environments",
        "services",
        "api_keys",
        "logs",
        "metrics",
        "traces",
        "service_dependencies",
        "anomalies",
        "incidents",
        "evidence",
        "root_cause_candidates",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_all_core_models_are_importable():
    models = [
        Organization,
        User,
        Membership,
        Environment,
        Service,
        APIKey,
        LogEvent,
        MetricPoint,
        TraceSpan,
        ServiceDependency,
        Anomaly,
        Incident,
        Evidence,
        RootCauseCandidate,
    ]

    assert len(models) == 14


def test_tenant_owned_models_have_organization_id():
    tenant_tables = [
        "memberships",
        "environments",
        "services",
        "api_keys",
        "logs",
        "metrics",
        "traces",
        "service_dependencies",
        "anomalies",
        "incidents",
        "evidence",
        "root_cause_candidates",
    ]

    for table_name in tenant_tables:
        assert "organization_id" in Base.metadata.tables[table_name].columns