from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.types import json_type


class CandidateProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "candidate_profiles"

    name: Mapped[str] = mapped_column(String(128))
    headline: Mapped[str | None] = mapped_column(String(255), nullable=True)
    base_info: Mapped[dict] = mapped_column(json_type, default=dict)
    availability_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    preferred_roles: Mapped[list] = mapped_column(json_type, default=list)


class PlatformRegistry(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "platform_registry"

    platform_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    platform_name: Mapped[str] = mapped_column(String(128))
    platform_family: Mapped[str] = mapped_column(String(64))
    platform_type: Mapped[str] = mapped_column(String(32))
    adapter_code: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    health_status: Mapped[str] = mapped_column(String(32), default="healthy")
    supported_actions: Mapped[list] = mapped_column(json_type, default=list)
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Device(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "devices"

    device_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    platform_type: Mapped[str] = mapped_column(String(32))
    device_name: Mapped[str] = mapped_column(String(128))
    adb_serial: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="idle")
    capabilities: Mapped[dict] = mapped_column(json_type, default=dict)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Job(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "jobs"

    platform_code: Mapped[str] = mapped_column(String(64), index=True)
    external_job_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    company_name: Mapped[str] = mapped_column(String(255))
    city: Mapped[str | None] = mapped_column(String(128), nullable=True)
    salary_text: Mapped[str | None] = mapped_column(String(128), nullable=True)
    recruiter_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    recruiter_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    job_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    job_snapshot: Mapped[dict] = mapped_column(json_type, default=dict)


class MessageTemplate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "message_templates"

    platform_code: Mapped[str] = mapped_column(String(64), index=True)
    scene_code: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(128))
    template_text: Mapped[str] = mapped_column(Text)
    variables: Mapped[list] = mapped_column(json_type, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class ApplicationTask(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "application_tasks"

    platform_code: Mapped[str] = mapped_column(String(64), index=True)
    platform_type: Mapped[str] = mapped_column(String(32))
    action_type: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    priority: Mapped[int] = mapped_column(default=0)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    device_id: Mapped[str] = mapped_column(ForeignKey("devices.id"))
    profile_id: Mapped[str] = mapped_column(ForeignKey("candidate_profiles.id"))
    message_template_id: Mapped[str | None] = mapped_column(ForeignKey("message_templates.id"), nullable=True)
    requires_manual_review: Mapped[bool] = mapped_column(Boolean, default=True)
    payload: Mapped[dict] = mapped_column(json_type, default=dict)
    worker_job_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    dispatched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    runs: Mapped[list[ApplicationRun]] = relationship(back_populates="task", cascade="all, delete-orphan")
    logs: Mapped[list[ApplicationLog]] = relationship(back_populates="task", cascade="all, delete-orphan")


class ApplicationRun(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "application_runs"

    task_id: Mapped[str] = mapped_column(ForeignKey("application_tasks.id"), index=True)
    driver_type: Mapped[str] = mapped_column(String(32))
    adapter_code: Mapped[str] = mapped_column(String(128))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    result: Mapped[str] = mapped_column(String(32), default="running")
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    screenshot_urls: Mapped[list] = mapped_column(json_type, default=list)
    trace_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_output: Mapped[dict] = mapped_column(json_type, default=dict)

    task: Mapped[ApplicationTask] = relationship(back_populates="runs")
    logs: Mapped[list[ApplicationLog]] = relationship(back_populates="run", cascade="all, delete-orphan")


class ApplicationLog(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "application_logs"

    task_id: Mapped[str] = mapped_column(ForeignKey("application_tasks.id"), index=True)
    run_id: Mapped[str | None] = mapped_column(ForeignKey("application_runs.id"), nullable=True, index=True)
    level: Mapped[str] = mapped_column(String(16), default="info")
    event_type: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(Text)
    details: Mapped[dict] = mapped_column(json_type, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    task: Mapped[ApplicationTask] = relationship(back_populates="logs")
    run: Mapped[ApplicationRun | None] = relationship(back_populates="logs")


class DedupeRecord(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "dedupe_records"

    platform_code: Mapped[str] = mapped_column(String(64), index=True)
    recruiter_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    action_type: Mapped[str] = mapped_column(String(64))
    dedupe_key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    last_executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
