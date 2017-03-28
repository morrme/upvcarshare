# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from users import UPVCARSHARE_GROUPS


def create_default_groups(sender, **kwargs):
    """Creates the default groups."""
    from django.contrib.auth.models import Group

    for group_name in UPVCARSHARE_GROUPS:
        group, _ = Group.objects.get_or_create(
            defaults={"name": group_name},
            name=group_name
        )
