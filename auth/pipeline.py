def staff_me_up(backend, details, response, uid, user, *args, **kwargs):
    user.is_staff = True
    user.save()
