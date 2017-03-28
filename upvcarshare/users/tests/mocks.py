# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

try:
    import unittest.mock as mock
except ImportError:
    import mock


class UPVLoginDataService(mock.MagicMock):

    PRESETS = {
        "margain": {
            "nombre": "Marcos",
            "apellidos": "Gabarda Inat",
            "dni": "53252985",
            "correo": "margain@upvnet.upv.es",
            "roles": ["EXTUPV", "UPVNET"],
            "centros": [],
            "titulaciones": []
        }
    }

    @classmethod
    def user_data(cls, username):
        return cls.PRESETS.get(username, {})
