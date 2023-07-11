from social_core.pipeline.social_auth import associate_by_email
from django.contrib.auth.models import Group


def staff_me_up(backend, details, response, uid, user, *args, **kwargs):
    user.is_staff = True
    try:
        user.groups.set([Group.objects.get(name="member")])
    except Group.DoesNotExist:
        pass
    user.save()


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
