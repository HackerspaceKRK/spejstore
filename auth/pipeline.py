from social_core.pipeline.social_auth import associate_by_email


def staff_me_up(backend, details, response, uid, user, *args, **kwargs):
    user.is_staff = True
    user.save()


def associate_by_personal_email(backend, details, user=None, *args, **kwargs):
    return associate_by_email(backend, {
        'email': details.get('personal_email'),
    }, user, *args, **kwargs)
