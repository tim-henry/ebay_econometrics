import csv
import matplotlib.pyplot as plt
import numpy as np
import os


def get_all_bids(directory):
    bids_l = []
    for i, auction in enumerate(os.listdir(directory)):
        f = directory + auction
        bids = {}
        with open(f, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if not (row[0]) in bids:
                    try:
                        bids[row[0]] = float(row[1][1:])
                    except:
                        pass
                else:
                    try:
                        bid = float(row[1][1:])
                        if bid > bids[row[0]]:
                            bids[row[0]] = bid
                    except:
                        pass
            b = set(bids.values())
            if len(b) == 0:
                continue
            bids_l.extend(b)
    return bids_l


def get_fraction_valid(directory):
    start_prices = np.zeros(385)
    winning_bids = np.zeros(385)
    winning_bid_auto = np.zeros(385, dtype=bool)
    count = 0
    for i, auction in enumerate(os.listdir(directory)):
        f = directory + auction
        with open(f) as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            row = next(reader)
            try:
                winning_bids[i] = float(row[1][1:])
                start_prices[i] = float(row[3][1:])
                winning_bid_auto[i] = row[4] == "True"
                count += 1
            except:
                pass
    return start_prices[winning_bids.nonzero()],\
           winning_bids[winning_bids.nonzero()],\
           winning_bid_auto[winning_bids.nonzero()]


def fit_and_plot(dist, values, ax):
    params = dist.fit(values)

    x = np.linspace(0, np.max(values) + 10, 100)
    ax.plot(x, dist.pdf(x, *params))

    p = dist.pdf(values, *params)
    mse = np.mean((values - p) ** 2)
    return mse, params


def get_weighted_bids(old_bids, start_prices):
    bids = []
    for i, bid in enumerate(old_bids):
        factor = np.sum(np.greater_equal(bid, start_prices)) / len(start_prices)
        bids.extend([bid] * int(np.round(1 / factor)))
    return bids


def plot_best_dist(values, name, distributions, plot_directory, experiment_name):
    fig, ax = plt.subplots()
    ax.hist(values, bins=20, density=True)

    best_mse = np.inf
    best_dist = None
    for dist in distributions:
        mse, _ = fit_and_plot(dist, values, ax)
        if mse < best_mse:
            best_mse = mse
            best_dist = dist

    print("====================================================================")
    print("BEST DIST for", name, best_dist)
    print("====================================================================")
    plt.title("Probability Density v. Price for various parametric distributions")
    plt.xlabel(name + " (USD)")
    plt.ylabel("Probability Density")
    plt.savefig(plot_directory + experiment_name + name + "_all_density.png")
    plt.show()
    plt.cla()
    plt.clf()

    rfig, ax = plt.subplots()
    h = ax.hist(values, bins=20, density=True)

    _, params = fit_and_plot(best_dist, values, ax)
    plt.title("Probability Density v. Price for best-fit distribution")
    plt.xlabel(name + " (USD)")
    plt.ylabel("Probability Density")
    plt.savefig(plot_directory + experiment_name + name + "_best_density.png")
    plt.show()
    plt.cla()
    plt.clf()
    return best_dist, params
