'''
  people class
'''

import random
import logging
import copy

from geopy.distance import geodesic


class People:
    '''
        people class
    '''

    PEOPLE_STATUS = ["victim", "patient"]
    GENDER = ["male", "female"]
    #China SH people square lattitude, longtitude
    POSITION = [31.23136, 121.47004]

    def __init__(self, **params):
        '''
            __init__
        '''
        self._id = params.get("id", 0)
        self._status = params.get("status", self.PEOPLE_STATUS[0])
        # location status
        self._startx = params.get("startx", self.POSITION[0])
        self._starty = params.get("starty", self.POSITION[1])
        self.step_length = params.get("step_length", 1)
        self._curx = params.get("curx", self.POSITION[0])
        self._cury = params.get("cury", self.POSITION[1])

        # features
        self.infected_period = params.get("infected_period", 0)
        self.disease_list = {}

        # herd features
        self.turn_over_rate = params.get("turn_over_rate", 50) # 50%
        self._gender  = params.get("gender", self.GENDER[0])
        self._age = params.get("age", 46)
        self.uhc = params.get("uhc", False) # with underlaying heal condition


    def time_pass(self):
        '''
            time pass
            attributes that need changed over period day
        '''
        if self._status == self.PEOPLE_STATUS[1]:
            self.infected_period += 1

        _turn_over = random.randint(0,100)
        if _turn_over < self.turn_over_rate:
            self.step_next_pos()

    def get_diseases(self):
        '''
            get_diseases
        '''
        return self.disease_list

    @property
    def is_infected(self):
        '''
            is_infected
        '''
        if self.status == "patient":
            return True
        return False

    @property
    def status(self):
        '''
            status
        '''
        return self._status

    @status.setter
    def status(self, value):
        '''
            setter for status
        '''
        self._status = value

    @property
    def id(self):
        '''
            status
        '''
        return self._id


    @property
    def cur_pos(self):
        '''
            cur_pos
        '''
        return (self._curx, self._cury)

    @cur_pos.setter
    def cur_pos(self, value):
        '''
            cur_pos setting
        '''
        self._curx = value[0]
        self._cury = value[1]

    def step_next_pos(self):
        '''
            step_next_pos
            step_x = 0.0000090198 ~ 1m
            step_y = 0.0000105 ~ 1m
            random direction
            [0, 1] -x
            (1, 2] +x
            (2, 3] -y
            (3, 4] +y
        '''
        _rd = random.randint(0,4)
        if _rd <= 1:
            self._curx -= 0.0000090198
        elif 1 < _rd <= 2:
            self._curx += 0.0000090198
        elif 2 < _rd <= 3:
            self._cury -= 0.0000105
        else:
            self._cury += 0.0000105

    def get_distant_from_start(self):
        '''
            get_distant_from_start
            step_x = 0.0000090198 ~ 1m
            step_y = 0.0000105 ~ 1m
        '''
        pos_a = (self._startx, self._starty)
        pos_b = (self._curx, self._cury)
        return geodesic(pos_a, pos_b).m

    def distant_from_you(self, another):
        '''
            calculate distance from another one
        '''
        pos_me = self.cur_pos
        pos_other = another.cur_pos
        return geodesic(pos_me, pos_other).m

    def infected_by_disease(self, disease):
        '''
            infected_by
            Param:
                disease class Disease: disease inst

            Return:
                NA
        '''
        if disease is None:
            return

        if disease.__class__.__name__ in self.disease_list:
            logging.info("already infected")
            return

        self.disease_list[disease.__class__.__name__] = copy.deepcopy(disease)
        self.infected_period = 1
        self._status = self.PEOPLE_STATUS[1]
        disease.r0 -= 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(filename)s:%(lineno)d] %(threadName)s %(message)s')
    p = People()
    logging.info("start")
    logging.info(p.get_distant_from_start())
