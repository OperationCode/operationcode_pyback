from typing import NamedTuple

""" Container for holding the pre-sent api requests """
ResponseContainer = NamedTuple('ResponseContainer', [('route', str), ('method', str), ('payload', dict)])
