'''
    infection operations
'''
import math

import logging


def to_latitude(m):
    '''
        latitude: 0.0000090198 ~ 1m
    '''
    return m * 0.0000090198

def to_longtitude(m):
    '''
        longtitude: 0.0000105 ~ 1m
    '''
    return m * 0.0000105

def distance_decay(d):
    '''
        distance_decay
    '''
    if d <= 2:
        return 1
    return math.exp(2 + (-1) * d)

def infection(p_a, p_b, **params):
    '''
		try to infect
		Param:
			p_a class Personal: person instance
			p_b class Personal: personal instance
			params dict: infection parameters
            the affect rate is calculated by:
            Ad = A0 * e ^^ (-d)
		retrun:
			True if infected
	'''
    if p_a.status == p_b.status:
        return False

    if p_a.id == p_b.id:
        return False

    p_a_diseases = p_a.get_diseases()
    p_b_diseases = p_b.get_diseases()

    infection_list_a = []
    infection_list_b = []

    environ_fact = params.get("fact", 1)

    _distance = p_a.distant_from_you(p_b)

    # A affects B
    for _d, _v in p_a_diseases.items():
        if _d not in p_b_diseases:
            if _v.infectious:
                infection_list_a.insert(-1, _v)

    for _d in infection_list_a:
        _real_rate = environ_fact * _d.r0 * distance_decay(_distance)
        logging.info("_real_rate is {}".format(_real_rate))
        logging.info("_distance is {}".format(_distance))
        if _real_rate >= 1:
            logging.info("infecting {} -> {}".format(p_a.id, p_b.id))
            p_b.infected_by_disease(_d)

    # B affects A
    for _d, _v in p_b_diseases.items():
        if _d not in p_a_diseases:
            if _v.infectious:
                infection_list_b.insert(-1, _v)

    for _d in infection_list_b:
        _real_rate = environ_fact * _d.r0 * distance_decay(_distance)
        if _real_rate >= 1:
            p_a.infected_by_disease(_d)
