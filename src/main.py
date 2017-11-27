import multiprocessing as mp
import sys
import numpy as np
import collections
from fitparse import FitFile

def get_timeoffset(start, timestamp):
    return 0 if start is None else int((timestamp - start).total_seconds())

def get_max_for_period(cumsum, period):
    windowsize = period*60
    maxpower = max((cumsum[windowsize:] - cumsum[:-windowsize]) / float(windowsize))
    return period, maxpower

def get_max_average_async(data, periods):
    result_list = []
    cumsum = np.cumsum(data)
    pool = mp.Pool()
    for period in periods:
        result_list.append(pool.apply_async(get_max_for_period, args=(cumsum, period , )).get())
    pool.close()
    pool.join()
    return result_list

def parse_fit_file(filename, fieldname):
    with open(filename, 'rb') as ffile:
        f'Opening and parsing fit file {filename}'
        fit = FitFile(ffile)
        start = None
        for message in fit.get_messages():
            if message.mesg_num == 0:
                start = message.get_value('time_created')
            elif message.mesg_num == 20 and message.get_value(fieldname) is not None:
                yield get_timeoffset(start, message.get_value('timestamp')), message.get_value(fieldname)
            
if __name__ == "__main__":
    print("Peaksware code test")
    if len(sys.argv) < 2:
        f'Usage: python {sys.argv[0]} <filename>'
        sys.exit(1)

    power_data = collections.OrderedDict({time_offset: power for time_offset, power in parse_fit_file(sys.argv[1], 'power')})
    print(get_max_average_async(list(power_data.values()), [1, 5, 10, 15, 20]))
