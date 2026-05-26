from app.models.entities import CandidateProfile, Job, MessageTemplate


def render_message_template(
    template: MessageTemplate | None,
    job: Job,
    profile: CandidateProfile,
) -> str:
    if template is None:
        return f"您好，我对您发布的{job.title}岗位很感兴趣，方便进一步沟通吗？"

    values = {
        "job_title": job.title,
        "company_name": job.company_name,
        "availability_date": profile.availability_date.isoformat() if profile.availability_date else "尽快",
        "profile_name": profile.name,
    }

    rendered = template.template_text
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered

