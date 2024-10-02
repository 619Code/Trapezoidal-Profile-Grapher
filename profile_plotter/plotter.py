import matplotlib.pyplot as plt
import csv
from pathlib import Path
import math

file_name = Path('test.csv')

def trapizoid_profile_abs(
        max_v: float,
        max_a: float,
        start_x: float,
        end_x: float,
        start_v: float):
    dx = abs(end_x - start_x)
    print(f'max_v = {max_v}, max_a = {max_a}, start_v = {start_v}')

    # 2 cases: trapezoid/triangle, or line
    if max_v > start_v:
        # We use start_v as a floor, then do the math as if it were zero
        tri_height = math.sqrt(max_a * dx)
        print(f"v_r = {tri_height}")
        
        if tri_height > max_v:
            # Trapezoid
            rel_v = max_v - start_v # This doesn't handle the case start_v > max_a
        else:
            # Triangle
            rel_v = tri_height - start_v # This doesn't handle the case start_v > max_a
            max_v = tri_height
        t1 = max(rel_v / max_a, 0)
        t2 = max((dx - (start_v * rel_v)/max_a) / (rel_v + start_v), 0)
    elif max_v == start_v:
        print("It's a line!")
        rel_v = 0
        max_v = start_v
        t1 = 0
        t2 = dx / start_v
        max_a = 0
    else:
        # How can I start faster than allowed?
        # Alternativly you could drop to the max_v,
        # but that would be a VERY jerky action
        raise Exception('start_v must be < max_v!')


    # In the triangluar case, we can effectively ignore t1
    if t1 > t2:
        t1 = t2

    # Find the inflection points so we have initial conditions
    # for the last 2 phases
    x_t1 = max_a * t1 * t1 / 2 + start_v * t1 + start_x
    x_t2 = x_t1 + max_v * (t2 - t1)

    print(f'x_t1 = {x_t1}, x_t2 = {x_t2}')

    print(f't1 = {t1}, t2= {t2}')

    # Define our time step
    dt = 0.02 # s

    # Set the initial conditions
    profile = [[0, start_x, start_v, max_a]] # (t, x, v, a)
    for t in [r * dt for r in range(1, math.ceil((t1 + t2) / dt) + 1)]:
        if t < t1:
            a_k = max_a
            v_k = a_k * t + start_v
            x_k = start_x + a_k * t * t / 2.0 + start_v * t
        elif t < t2:
            a_k = 0
            v_k = max_v
            x_k = x_t1 + v_k * (t- t1)
        elif t >= t2:
            offset_t = t - t2
            a_k = -max_a
            v_k = max_v - (max_a * (t - t2))
            x_k = x_t2 + max_v * offset_t + a_k * offset_t * offset_t / 2.0

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
    trapizoid_profile_abs(25, 10, 0, 20, 0)

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