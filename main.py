import numpy as np
import time
from model import TPM

k = 20
n = 5
l = 6

update_rules = ["hebbian", "anti_hebbian", "random_walk"]
update_rule = update_rules[0]

Alice = TPM(n, k, l)
Bob = TPM(n, k, l)


def random():
    return np.random.randint(-l, l+1, [k, n])


def random_one():
    rand = np.random.randint(0, 2, [k, n])
    for (i, j), _ in np.ndenumerate(rand):
        if rand[i, j] == 0:
            rand[i, j] = -1
    return rand


def sync_score(m1, m2):
    return 1.0 - np.average(1.0 * np.abs(m1.weights - m2.weights) / (2 * l))


sync = False
nb_updates = 0
start_time = time.time()
sync_history = []

while not sync:
    input_val = random()
    tauA = Alice(input_val)
    tauB = Bob(input_val)

    Alice.update(tauB, update_rule)
    Bob.update(tauA, update_rule)
    nb_updates += 1

    score = 100 * sync_score(Alice, Bob)

    sync_history.append(score)
    print(f"\rSynchronizatipn = {int(score)}% / Updates = {nb_updates}")
    if score == 100:
        sync = True

end_time = time.time()
time_taken = end_time - start_time

print("Machines have been synchronized.")
print(f"Time taken = {time_taken} seconds.")
print(f"Updates = {nb_updates}.")

import matplotlib.pyplot as mpl

mpl.plot(sync_history)
mpl.show()
