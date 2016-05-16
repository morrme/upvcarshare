# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import


class NoFreePlaces(Exception):
    msg = "No free places for this journey."


class AlreadyAPassenger(Exception):
    msg = "User is already a passenger."


class NotAPassenger(Exception):
    msg = "The user is not a passenger of this journey."
