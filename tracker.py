import folium


import random
import logging

import people
import disease

from interface import *


PEOPLE_SQUARE = [31.23136, 121.47004]


def create_people_with_disease(id_start):
    '''
        create_people_with_disease
    '''
    params = {"id" : id_start}
    _p = people.People(**params)
    _d = disease.Disease()
    _p.infected_by_disease(_d)
    logging.info("recv time init is {}".format(_d.recv_time))
    return _p

# create n of people at random position in given region
def cal_pos(n, p, rect, start_point):
    '''
        cal pos for n in region
    '''
    peoples = []
    plist = []
    id_count = 0
    total_size = rect[0] * rect[1]
    for i in range(total_size):
        plist += [i]

    final_list = []
    i = total_size
    while i > total_size - n:
        d = random.randint(0, i)
        try:
            final_list.insert(-1, plist[d])
            del plist[d]
        except:
            logging.info("d {} error".format(d))
        i -= 1

    logging.info(final_list)

    x_len = rect[0]
    for i in final_list:
        _ix = to_latitude(i % x_len)
        _iy = to_longtitude(i / x_len)

        pos = {"curx" : _ix + start_point[0],
                "cury" : _iy + start_point[1],
                "id": id_count
              }
        logging.info(pos)
        _ps = people.People(**pos)
        peoples.insert(-1, _ps)
        id_count += 1

    final_list_p = []
    i = total_size - n
    while i > total_size - n - p:
        d = random.randint(0, i)
        final_list_p.insert(-1, plist[d])
        del plist[d]
        i -= 1

    for i in final_list_p:
        _ix = to_latitude(i % x_len)
        _iy = to_longtitude(i / x_len)

        pos = (_ix + start_point[0],
               _iy + start_point[1])
        logging.info(pos)
        _ps = create_people_with_disease(n)
        _ps.cur_pos = pos
        peoples.insert(-1, _ps)

    return peoples


def place_peoples(m, peoples):
    '''
        place peoples on m map
    '''

    for _p in peoples:
        if _p.status == "victim":
            folium.Marker(
                location = _p.cur_pos,
                popup="victim",
                icon=folium.Icon(color="green", icon="info-sign"),
            ).add_to(m)
        else:
            folium.Marker(
                location = _p.cur_pos,
                popup = "patient",
                icon = folium.Icon(color="red", icon="info-sign"),
            ).add_to(m)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(filename)s:%(lineno)d] %(threadName)s %(message)s')
    _ps = cal_pos(9, 1, [20, 20], PEOPLE_SQUARE)
    for _p in _ps:
        logging.info("==============")
        logging.info("\tid is {}".format(_p.id))
        logging.info("\t status is {}".format(_p.status))

    _m0 = folium.Map(location=PEOPLE_SQUARE, zoom_start=20)
    place_peoples(_m0, _ps)
    _m0.save("index_ori.html")
    loops = 5000
    for i in range(loops):
        # assume 500 steps is a day
        _is_day = False
        if i > 500 and i% 500 == 0:
            logging.info("day {}".format(i/500))
            _is_day = True
        for _p in _ps:
            if _is_day:
                _p.time_pass(True)
            else:
                _p.time_pass()
        for _pa in _ps:
            for _pb in _ps:
                _ret = infection(_pa, _pb)
                if _ret:
                    logging.info("step: {}".format(i))
    _p_c = 0
    _p_i = 0
    for _p in _ps:
        logging.info("==============")
        logging.info("\tid is {}".format(_p.id))
        logging.info("\t status is {}".format(_p.status))
        _des = _p.get_diseases()
        for _d, _v in _des.items():
            logging.info("\t recv time is {}".format(_v.recv_time))
        if _p.is_infected:
            _p_c += 1
        if len(_p.infected_history) > 0:
            _p_i += 1

    logging.info("alt {} people currently illed".format(_p_c))
    logging.info("alt {} people get infected".format(_p_i))
    convert_pair_to_tree()
    _m = folium.Map(location=PEOPLE_SQUARE, zoom_start=20)
    place_peoples(_m, _ps)
    _m.save("index.html")
