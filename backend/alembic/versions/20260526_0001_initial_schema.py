"""create initial schema

Revision ID: 20260526_0001
Revises:
Create Date: 2026-05-26 21:15:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

from app.models.types import json_type


revision = "20260526_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "candidate_profiles",
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("headline", sa.String(length=255), nullable=True),
        sa.Column("base_info", json_type, nullable=False),
        sa.Column("availability_date", sa.Date(), nullable=True),
        sa.Column("preferred_roles", json_type, nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "platform_registry",
        sa.Column("platform_code", sa.String(length=64), nullable=False),
        sa.Column("platform_name", sa.String(length=128), nullable=False),
        sa.Column("platform_family", sa.String(length=64), nullable=False),
        sa.Column("platform_type", sa.String(length=32), nullable=False),
        sa.Column("adapter_code", sa.String(length=128), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("health_status", sa.String(length=32), nullable=False),
        sa.Column("supported_actions", json_type, nullable=False),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_platform_registry_platform_code"), "platform_registry", ["platform_code"], unique=True)
    op.create_table(
        "devices",
        sa.Column("device_code", sa.String(length=64), nullable=False),
        sa.Column("platform_type", sa.String(length=32), nullable=False),
        sa.Column("device_name", sa.String(length=128), nullable=False),
        sa.Column("adb_serial", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("capabilities", json_type, nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_devices_device_code"), "devices", ["device_code"], unique=True)
    op.create_table(
        "jobs",
        sa.Column("platform_code", sa.String(length=64), nullable=False),
        sa.Column("external_job_id", sa.String(length=128), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=128), nullable=True),
        sa.Column("salary_text", sa.String(length=128), nullable=True),
        sa.Column("recruiter_name", sa.String(length=128), nullable=True),
        sa.Column("recruiter_id", sa.String(length=128), nullable=True),
        sa.Column("job_url", sa.Text(), nullable=True),
        sa.Column("job_snapshot", json_type, nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_jobs_platform_code"), "jobs", ["platform_code"], unique=False)
    op.create_table(
        "message_templates",
        sa.Column("platform_code", sa.String(length=64), nullable=False),
        sa.Column("scene_code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("template_text", sa.Text(), nullable=False),
        sa.Column("variables", json_type, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "application_tasks",
        sa.Column("platform_code", sa.String(length=64), nullable=False),
        sa.Column("platform_type", sa.String(length=32), nullable=False),
        sa.Column("action_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.String(length=36), nullable=False),
        sa.Column("device_id", sa.String(length=36), nullable=False),
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("message_template_id", sa.String(length=36), nullable=True),
        sa.Column("requires_manual_review", sa.Boolean(), nullable=False),
        sa.Column("payload", json_type, nullable=False),
        sa.Column("worker_job_id", sa.String(length=64), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"]),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"]),
        sa.ForeignKeyConstraint(["message_template_id"], ["message_templates.id"]),
        sa.ForeignKeyConstraint(["profile_id"], ["candidate_profiles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_application_tasks_platform_code"), "application_tasks", ["platform_code"], unique=False)
    op.create_index(op.f("ix_application_tasks_status"), "application_tasks", ["status"], unique=False)
    op.create_table(
        "application_runs",
        sa.Column("task_id", sa.String(length=36), nullable=False),
        sa.Column("driver_type", sa.String(length=32), nullable=False),
        sa.Column("adapter_code", sa.String(length=128), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("result", sa.String(length=32), nullable=False),
        sa.Column("error_code", sa.String(length=64), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("screenshot_urls", json_type, nullable=False),
        sa.Column("trace_url", sa.Text(), nullable=True),
        sa.Column("raw_output", json_type, nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["task_id"], ["application_tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_application_runs_task_id"), "application_runs", ["task_id"], unique=False)
    op.create_table(
        "application_logs",
        sa.Column("task_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=True),
        sa.Column("level", sa.String(length=16), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details", json_type, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], ["application_runs.id"]),
        sa.ForeignKeyConstraint(["task_id"], ["application_tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_application_logs_run_id"), "application_logs", ["run_id"], unique=False)
    op.create_index(op.f("ix_application_logs_task_id"), "application_logs", ["task_id"], unique=False)
    op.create_table(
        "dedupe_records",
        sa.Column("platform_code", sa.String(length=64), nullable=False),
        sa.Column("recruiter_id", sa.String(length=128), nullable=True),
        sa.Column("job_id", sa.String(length=36), nullable=False),
        sa.Column("action_type", sa.String(length=64), nullable=False),
        sa.Column("dedupe_key", sa.String(length=255), nullable=False),
        sa.Column("last_executed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dedupe_records_dedupe_key"), "dedupe_records", ["dedupe_key"], unique=True)
    op.create_index(op.f("ix_dedupe_records_platform_code"), "dedupe_records", ["platform_code"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_dedupe_records_platform_code"), table_name="dedupe_records")
    op.drop_index(op.f("ix_dedupe_records_dedupe_key"), table_name="dedupe_records")
    op.drop_table("dedupe_records")
    op.drop_index(op.f("ix_application_logs_task_id"), table_name="application_logs")
    op.drop_index(op.f("ix_application_logs_run_id"), table_name="application_logs")
    op.drop_table("application_logs")
    op.drop_index(op.f("ix_application_runs_task_id"), table_name="application_runs")
    op.drop_table("application_runs")
    op.drop_index(op.f("ix_application_tasks_status"), table_name="application_tasks")
    op.drop_index(op.f("ix_application_tasks_platform_code"), table_name="application_tasks")
    op.drop_table("application_tasks")
    op.drop_table("message_templates")
    op.drop_index(op.f("ix_jobs_platform_code"), table_name="jobs")
    op.drop_table("jobs")
    op.drop_index(op.f("ix_devices_device_code"), table_name="devices")
    op.drop_table("devices")
    op.drop_index(op.f("ix_platform_registry_platform_code"), table_name="platform_registry")
    op.drop_table("platform_registry")
    op.drop_table("candidate_profiles")
