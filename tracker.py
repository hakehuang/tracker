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

    logging.info(final_list_p)

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
    _ps = cal_pos(9, 1, [50, 50], PEOPLE_SQUARE)
    for _p in _ps:
        logging.info("==============")
        logging.info("\tid is {}".format(_p.id))
        logging.info("\t status is {}".format(_p.status))

    _m0 = folium.Map(location=PEOPLE_SQUARE, zoom_start=20)
    place_peoples(_m0, _ps)
    _m0.save("index_ori.html")
    loops = 1000
    for i in range(loops):
        for _p in _ps:
            _p.time_pass()
        for _pa in _ps:
            for _pb in _ps:
                infection(_pa, _pb)
    _p_c = 0
    for _p in _ps:
        logging.info("==============")
        logging.info("\tid is {}".format(_p.id))
        logging.info("\t status is {}".format(_p.status))
        if _p.is_infected:
            _p_c += 1
    logging.info("alt {} people get infected".format(_p_c))
    _m = folium.Map(location=PEOPLE_SQUARE, zoom_start=20)
    place_peoples(_m, _ps)
    _m.save("index.html")
