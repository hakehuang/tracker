'''
    disease
'''
import logging

class Disease:
    '''
        disease
    '''
    def __init__(self, **params):
        '''
            __init__
        '''
        self._r0 = params.get("r0", 6)
        self._re = params.get("re", 20) # 20%
        self._incubation_period = params.get("incubation_period", 1) # in days
        self._typical_recover_time = params.get("typical_recover_time", 14) # in days
        self._death_rate = params.get("death_rate", 1) # 1%
        self.infectious = params.get("infectious", True)
        self._nature_immunity_period = 180

    @property
    def immunity_period(self):
        '''
            immunity_period
        '''
        return self._nature_immunity_period

    @property
    def r0(self):
        '''
            r0
        '''
        return self._r0

    @r0.setter
    def r0(self, value):
        '''
            r0 setting
        '''
        self._r0 = value

    @property
    def recv_time(self):
        '''
            typical_recover
        '''
        return self._typical_recover_time

    @recv_time.setter
    def recv_time(self, value):
        '''
            typical_recover setting
        '''
        self._typical_recover_time = value
