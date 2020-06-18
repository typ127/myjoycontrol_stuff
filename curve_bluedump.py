import argparse
import struct
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

    last_timestamp = 0
    plotTimeIn = []
    plotValueIn = []
    plotTimeOut = []
    plotValueOut = []

    lineFrom = 0
    lineTo = 900
    count = 0


    with open(args.dumpfile, 'r') as dumpfile:
        lines = dumpfile.readlines()[lineFrom:lineTo]
        for line in lines:
            if not line.startswith('\t'):
                strTimestamp = line.split(" ")[0]
                inout = line.split(" ")[5]
                length = line.split(" ")[3]
                if strTimestamp != '\n':
                    print(strTimestamp, length, inout)
                    dt = datetime.strptime("20.12.2016 "+strTimestamp, "%d.%m.%Y %H:%M:%S.%f")
                    timestamp = datetime.timestamp(dt)
                    if inout.startswith('in'):
                        if length == '8,':
                            plotTimeIn.append(timestamp)
                            plotValueIn.append(count)
                    else:
                        plotTimeOut.append(timestamp)
                        plotValueOut.append(count+100)

                    count += 1

    plt.plot(plotTimeIn, plotValueIn, 'rx', plotTimeOut, plotValueOut, 'bo')
    plt.savefig('curve_inout_noreportout.png')




