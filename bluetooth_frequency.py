import argparse
from datetime import datetime
import matplotlib.pyplot as plt

"""

plots distances between neighboured timestamps. This should sow
the input report frequency ideally (e.g. line at 0.015 seconds)

"""
def eof_read(file, size):
    """
    Raises EOFError if end of file is reached.
    """
    data = file.read(size)
    if not data:
        raise EOFError()
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dumpfile')
    args = parser.parse_args()

    last_timestamp_in = 0
    last_timestamp_out = 0
    plotTimeIn = []
    plotValueIn = []
    plotTimeOut = []
    plotValueOut = []

    lineFrom = 0
    lineTo = 2200
    count = 0

    with open(args.dumpfile, 'r') as dumpfile:
        lines = dumpfile.readlines()[lineFrom:lineTo]
        for line in lines:
            if not line.startswith('\t'):
                strTimestamp = line.split(" ")[0]
                inout = line.split(" ")[5]
                if strTimestamp != '\n':
                    print(strTimestamp, inout)
                    dt = datetime.strptime("20.12.2016 "+strTimestamp, "%d.%m.%Y %H:%M:%S.%f")
                    timestamp = datetime.timestamp(dt)
                    if inout.startswith('in'):
                        if last_timestamp_in > 0:
                            d = timestamp - last_timestamp_in
                            plotTimeIn.append(timestamp)
                            plotValueIn.append(d)
                        last_timestamp_in = timestamp
                    else:
                        if last_timestamp_out > 0:
                            d = timestamp - last_timestamp_out
                            plotTimeOut.append(timestamp)
                            plotValueOut.append(d)
                        last_timestamp_out = timestamp

    marker_in = dict(color='red', linestyle = '', marker = 'o', markersize = 2)
    plt.plot(plotTimeIn, plotValueIn, **marker_in)
    plt.plot(plotTimeOut, plotValueOut, 'b.')
    plt.savefig('frequency_inout_66_100.png')
