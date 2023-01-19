import numpy as np
import time
from model import TPM
import matplotlib.pyplot as mpl

k = 20
n = 5
max_value = 6

update_rules = ["hebbian", "anti_hebbian", "random_walk"]
update_rule = update_rules[0]

Alice = TPM(n, k, max_value)
Bob = TPM(n, k, max_value)
Eve = TPM(n, k, max_value)


def random():
    return np.random.randint(-max_value, max_value + 1, [k, n])


def random_one():
    rand = np.random.randint(0, 2, [k, n])
    for (i, j), _ in np.ndenumerate(rand):
        if rand[i, j] == 0:
            rand[i, j] = -1
    return rand


def sync_score(m1, m2):
    return 1.0 - np.average(1.0 * np.abs(m1.weights - m2.weights) / (2 * max_value))


sync = False
nb_updates = 0
nb_eve_updates = 0
start_time = time.time()
sync_history = []
eve_sync_history = []

while not sync:
    input_val = random()

    tauA = Alice(input_val)
    tauB = Bob(input_val)
    tauE = Eve(input_val)

    Alice.update(tauB, update_rule)
    Bob.update(tauA, update_rule)

    if tauA == tauB == tauE:
        Eve.update(tauA, update_rule)
        nb_eve_updates += 1

    nb_updates += 1

    score = 100 * sync_score(Alice, Bob)
    sync_history.append(score)

    eve_score = 100 * sync_score(Alice, Eve)
    eve_sync_history.append(eve_score)

    print(f"\rSynchronization = {int(score)}% / Updates = {nb_updates}")

    if score == 100:
        sync = True

end_time = time.time()
time_taken = end_time - start_time

print("Machines have been synchronized.")
print(f"Time taken = {time_taken} seconds.")
print(f"Updates = {nb_updates}.")

eve_score = 100 * sync_score(Alice, Eve)

if eve_score > 100:
    print(f"Eve synchronized her machine with Alice's and Bob's !")
else:
    print(f"Eve's machine is only {eve_score}% synced with Alice's and Bob's and she did {nb_eve_updates} updates.")


mpl.plot(sync_history)
mpl.plot(eve_sync_history)
mpl.show()
