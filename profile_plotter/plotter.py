import matplotlib.pyplot as plt
import csv
from pathlib import Path
import argparse

def main():

    parser = argparse.ArgumentParser(
                    prog='Profile Grapher',
                    description='Reads a .csv file and graphs the position, velocity, acceleration',
                    epilog='')

    parser.add_argument(
        'filename'
    )

    args = parser.parse_args()

    file_name = Path(args.filename)

    # TODO make this more flexible
    t = []
    x = []
    v = []
    a = []
    # Read in all the points
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, skipinitialspace=True)
        for line in reader:
            t.append(float(line[0]))
            x.append(float(line[1]))
            v.append(float(line[2]))
            a.append(float(line[3]))

    # Plot them out
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    fig.suptitle(f'Data from {file_name}')

    # position
    ax1.plot(t, x)
    ax1.set_ylabel('x')

    # velocity
    ax2.plot(t, v)
    ax2.set_ylabel('v')

    # acceleration
    ax3.plot(t, a)
    ax3.set_xlabel('t')
    ax3.set_ylabel('a')

    plt.show()

if __name__ == '__main__':
    main()