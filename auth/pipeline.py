from social_core.pipeline.social_auth import associate_by_email
from django.contrib.auth.models import Group


def associate_by_personal_email(backend, details, user=None, *args, **kwargs):
    return associate_by_email(
        backend,
        {
            "email": details.get("personal_email"),
        },
        user,
        *args,
        **kwargs
    )
