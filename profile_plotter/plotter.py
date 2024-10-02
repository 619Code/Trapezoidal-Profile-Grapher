import matplotlib.pyplot as plt
import csv
from pathlib import Path
import math

file_name = Path('test.csv')

def trapizoid_profile_abs(max_v: int, max_a: int, start_x: int, end_x: int):
    profile = [[0, start_x, 0, max_a]] # (t, x, v, a)
    dx = abs(end_x - start_x)
    max_v = min(max_v, max_a)
    t1 = max_v / max_a
    t2 = dx / max_v

    # In the triangluar case, we can effectively ignore t1
    if t1 > t2:
        t1 = t2

    # Find the initial conditions for the const vel and deccel
    x_t1 = max_a * t1 * t1 / 2 + start_x
    v_t1 = max_a * t1
    x_t2 = x_t1 + max_v * (t2 - t1) # TODO what if you don't hit max_v
    v_t2 = v_t1

    print(f'x_t1 = {x_t1}, x_t2 = {x_t2}')

    print(f't1 = {t1}, t2= {t2}')

    dt = 0.02 # s
    for t in [r * dt for r in range(1, math.ceil((t1 + t2) / dt) + 1)]:
        last_point = profile[-1]
        if t < t1:
            x_k = start_x + max_a * t * t / 2.0
            v_k = max_a * t
            a_k = max_a
        elif t < t2:
            x_k = x_t1 + max_v * (t- t1)
            v_k = max_v
            a_k = 0
        elif t >= t2:
            offset_t = t - t2
            x_k = x_t2 + max_v * offset_t + -max_a * offset_t * offset_t / 2.0
            v_k = max_v - (max_a * (t - t2))
            a_k = -max_a

        profile.append([t, x_k, v_k, a_k])

    with open(file_name, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for pt in profile:
            writer.writerow(pt)

def trapizoid_profile_rel(max_v: int, max_a: int, start_x: int, end_x: int):
    profile = [[0, start_x, 0, max_a]] # (t, x, v, a)
    dx = abs(end_x - start_x)
    max_v = min(max_v, max_a)
    t1 = max_v / max_a
    t2 = dx / max_v
    # In the triangluar case, we can effectively ignore t1
    if t1 > t2:
        t1 = t2

    print(f't1 = {t1}, t2= {t2}')

    dt = 0.02 # s
    for t in [r * dt for r in range(1, math.ceil((t1 + t2) / dt) + 1)]:
        last_point = profile[-1]
        if t < t1:
            x_k = last_point[2]*dt + last_point[1] # v_k-1 * t + x_k-1
            v_k = last_point[3]*dt + last_point[2] # a_k-1 * t + v_k-1
            a_k = max_a
        elif t < t2:
            x_k = last_point[2]*dt + last_point[1] #v_k-1 * t + x_k-1
            v_k = last_point[2] # v_k-1
            a_k = 0
        elif t >= t2:
            x_k = last_point[2]*dt + last_point[1] #v_k-1 * t + x_k-1
            v_k = last_point[3]*dt + last_point[2] # a_k-1 * t + v_k-1
            a_k = -max_a

        profile.append([t, x_k, v_k, a_k])

    with open(file_name, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for pt in profile:
            writer.writerow(pt)


def profile():
    # trapizoid_profile_rel(20, 30, 0, 20)
    trapizoid_profile_abs(15, 50, 0, 20)

def main():

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