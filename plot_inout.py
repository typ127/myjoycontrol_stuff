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

    first_timestamp = 1482261865

    lineFrom = 1650
    lineTo = 1850
    count = 0

    with open(args.dumpfile, 'r') as dumpfile:
        lines = dumpfile.readlines()[lineFrom:lineTo]
        for line in lines:
            if not line.startswith('\t'):
                strTimestamp = line.split(" ")[0]
                inout = line.split(" ")[5].split('\n')[0]
                length = int(line.split(" ")[3].split(',')[0])
                if length > 100:
                    length = 100
                if strTimestamp != '\n':
#                    print(strTimestamp, length, inout)
                    dt = datetime.strptime("20.12.2016 "+strTimestamp, "%d.%m.%Y %H:%M:%S.%f")
                    timestamp = datetime.timestamp(dt) - first_timestamp
                    print(timestamp, length, inout)
                    if inout.startswith('in'):
                        plotTimeIn.append(timestamp)
                        plotValueIn.append(length)
                    else:
                        plotTimeOut.append(timestamp)
                        plotValueOut.append(length)

    marker_in = dict(color='red', linestyle = '', marker = '.', markersize = 3)
    marker_out = dict(color='blue', linestyle = '', marker = '.', markersize = 3)
    plt.plot(plotTimeIn, plotValueIn, **marker_in)
    plt.plot(plotTimeOut, plotValueOut, **marker_out)
    plt.savefig('frequency_inout_66_100_D.png')
