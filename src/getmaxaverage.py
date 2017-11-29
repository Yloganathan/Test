import multiprocessing as mp
import sys
from numpy import cumsum as runningsum
from collections import OrderedDict
from fitparse import FitFile

def get_timeoffset(start, timestamp):
    return 0 if start is None else int((timestamp - start).total_seconds())

def get_max_for_period(running_sum, period):
    # TODO: try dequeue or dynamic programming to see if it saves time
    windowsize = period*60
    maxpower = max((running_sum[windowsize:] - running_sum[:-windowsize]) / float(windowsize))
    return period, maxpower

def get_max_average_for_periods(data, periods):
    # TODO: Identify if this is the best way to do handle async for this problem
    results = []
    running_sum = runningsum(data)
    pool = mp.Pool()
    for period in periods:
        pool.apply_async(get_max_for_period, args=(running_sum, period , ), callback=results.append)
    pool.close()
    pool.join()
    return results

def parse_fit_file(filename, fieldname):
    with open(filename, 'rb') as ffile:
        print(f'Opening and parsing fit file {filename}')
        fit = FitFile(ffile)
        start = None
        for message in fit.get_messages():
            if message.mesg_num == 0:
                start = message.get_value('time_created')
            elif message.mesg_num == 20 and message.get_value(fieldname) is not None:
                yield get_timeoffset(start, message.get_value('timestamp')), message.get_value(fieldname)


def get_max_power_average(filename):
    # TODO: Update code to fill in the missing seconds? 
    seconds_to_power = OrderedDict({time_offset: power for time_offset, power in parse_fit_file(sys.argv[1], 'power')})
    print(get_max_average_for_periods(list(seconds_to_power.values()), [1, 5, 10, 15, 20]))

            
if __name__ == "__main__":
    print("Peaksware code test")
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <filename>')
        sys.exit(1)

    get_max_power_average(sys.argv[1])
