# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import requests
from django.conf import settings
from django.contrib.auth.models import Group

from users import UPV_STUDENT_ROLES, STUDENTS_GROUP, STAFF_GROUP


class UPVLoginDataService(object):
    """Class to access to data user from UPV."""

    BASE_URL = "https://piolin.upv.es/consultas/?c=datosLG1"

    @classmethod
    def credentials(cls):
        user = settings.UPV_LOGIN_DATA_USERNAME
        password = settings.UPV_LOGIN_DATA_PASSWORD
        return user, password

    @classmethod
    def user_data(cls, username):
        response = requests.post(
            url=cls.BASE_URL,
            data={
                "login": username
            },
            auth=cls.credentials()
        )
        if response != 200:
            return {}
        return response.json()


def from_roles_to_groups(roles):
    """Uses UPV roles to select the correct internal group. Returns always a list of 
    groups, even if it's now fixed to a single one.
    """
    try:
        roles = [] if roles is None else roles
        if set(roles).intersection(set(UPV_STUDENT_ROLES)):
            return [Group.objects.get(name=STUDENTS_GROUP)]
        return [Group.objects.get(name=STAFF_GROUP)]
    except Group.DoesNotExist:
        return list()
