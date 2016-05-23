# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import floppyforms


class OsmPointWidget(floppyforms.gis.BaseOsmWidget, floppyforms.gis.PointWidget):
    pass


class GMapsPointWidget(floppyforms.gis.BaseGMapWidget, floppyforms.gis.PointWidget):
    pass
