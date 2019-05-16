import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.stats as st


# =====================================================================================================================


EXPERIMENT_NAME = ""
DATA_DIRECTORY = "../auction_data/"
PLOT_DIRECTORY = "../plots/"
DISTRIBUTIONS = [
    st.dgamma, st.dweibull, st.cauchy, st.vonmises_line,
    st.alpha, st.anglit, st.betaprime, st.bradford, st.chi, st.cosine, st.exponnorm, st.f, st.foldnorm, st.genlogistic,
    st.genpareto, st.genexpon, st.gausshyper, st.genhalflogistic, st.gilbrat, st.gumbel_r, st.gumbel_l, st.halfcauchy,
    st.halflogistic, st.halfnorm, st.hypsecant, st.invgamma, st.invgauss, st.invweibull, st.johnsonsb, st.johnsonsu,
    st.ksone, st.kstwobign, st.logistic, st.loggamma, st.loglaplace, st.maxwell, st.mielke, st.nct, st.norm,
    st.powerlaw, st.reciprocal, st.rayleigh, st.rice, st.semicircular, st.t, st.triang, st.truncexpon, st.truncnorm,
    st.tukeylambda, st.uniform,  st.wald, st.wrapcauchy
]


# =====================================================================================================================


def get_all_bids():
    bids_l = []
    for i, auction in enumerate(os.listdir(DATA_DIRECTORY)):
        f = DATA_DIRECTORY + auction
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


def get_fraction_valid():
    start_prices = np.zeros(385)
    winning_bids = np.zeros(385)
    winning_bid_auto = np.zeros(385, dtype=bool)
    count = 0
    for i, auction in enumerate(os.listdir(DATA_DIRECTORY)):
        f = DATA_DIRECTORY + auction
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


def plot_best_dist(values, name):
    fig, ax = plt.subplots()
    ax.hist(values, bins=20, density=True)

    best_mse = np.inf
    best_dist = None
    for dist in DISTRIBUTIONS:
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
    plt.savefig(PLOT_DIRECTORY + EXPERIMENT_NAME + name + "_all_density.png")
    plt.show()
    plt.cla()
    plt.clf()

    rfig, ax = plt.subplots()
    h = ax.hist(values, bins=20, density=True)

    _, params = fit_and_plot(best_dist, values, ax)
    plt.title("Probability Density v. Price for best-fit distribution")
    plt.xlabel(name + " (USD)")
    plt.ylabel("Probability Density")
    plt.savefig(PLOT_DIRECTORY + EXPERIMENT_NAME + name + "_best_density.png")
    plt.show()
    plt.cla()
    plt.clf()
    return best_dist, params


# =====================================================================================================================


# Get raw data
start_prices, winning_bids, winning_bid_auto = get_fraction_valid()
old_bids = np.array(get_all_bids())

# Extrapolate to bids below start price
bids = get_weighted_bids(old_bids, start_prices)

# Find best parametric distribution
best_bid_dist, best_bid_params = plot_best_dist(bids, "Bids")
plot_best_dist(start_prices, "Auction Start Price")
plot_best_dist(winning_bids, "Winning Bids")

# Plot winning bids
plt.hist(winning_bids, bins=range(int(np.min(winning_bids)), int(np.max(winning_bids)), 20), density=True)
plt.ylim(0, 0.03)
plt.title("Winning Bids")
plt.savefig(PLOT_DIRECTORY + EXPERIMENT_NAME + "winning_bid_dist_empirical.png")
plt.show()
plt.clf()
plt.cla()


# =====================================================================================================================


def generate_n_samples(n, dist, params):
    samples = np.array(dist.rvs(*params, size=n * 5))
    return np.round(samples[samples >= 0][:n + 1])


def generate_auction(i, n_bidders, bid_dist, bid_params, depth=0):
    start_price = start_prices[i]
    bids = sorted(generate_n_samples(n_bidders, bid_dist, bid_params))
    highest = bids[-1]
    if depth > 3:
        return start_price, bids, None
    if highest > start_price:
        return start_price, bids, highest
    else:
        return generate_auction(i, n_bidders, bid_dist, bid_params, depth=depth + 1)


def generate_n_auctions(n_bidders, n_auctions, bid_dist, bid_params):
    sim_start_prices = []
    sim_sale_prices = []
    for i in range(n_auctions):
        start_price, _, sale_price = generate_auction(i, n_bidders, bid_dist, bid_params)
        sim_start_prices.append(start_price)
        sim_sale_prices.append(sale_price)
    return sim_start_prices, sim_sale_prices


def plot_hist_of_sims(sale_prices):
    fig, ax = plt.subplots()
    sale_prices = np.array(sale_prices)
    sale_prices = sale_prices[sale_prices != np.array(None)]
    sale_prices = sale_prices.astype(int)
    ax.hist(sale_prices, bins=range(int(np.min(winning_bids)), int(np.max(winning_bids)), 20), density=True)
    plt.ylim(0, 0.03)
    plt.title("Simulated Winning Bids")
    plt.savefig(PLOT_DIRECTORY + EXPERIMENT_NAME + "winning_bid_dist_sim.png")
    plt.show()
    plt.clf();
    plt.cla()


# =====================================================================================================================


# Generate auctions
n_bidders, n_auctions = 7, 380
first_price_prob = 1 - (np.sum(winning_bid_auto) / len(winning_bid_auto))
sim_start_prices, sim_winning_bids = generate_n_auctions(n_bidders, n_auctions, best_bid_dist, best_bid_params)
plot_hist_of_sims(sim_winning_bids)

# Plot relationship between winning bids and start prices
plt.scatter(start_prices, winning_bids)
plt.title("Winning Bid v. Start Price (empirical)")
plt.xlabel("Start Price")
plt.ylabel("Winning Bid")
plt.xlim(0, 450)
plt.ylim(0, 650)
plt.savefig(PLOT_DIRECTORY + EXPERIMENT_NAME + "win_v_start_empirical.png")
plt.show()
plt.clf(); plt.cla()

# Plot simulated relationship between winning bids and start prices
plt.scatter(sim_start_prices, sim_winning_bids)
plt.title("Simulated Winning Bid v. Start Price")
plt.xlabel("Start Price")
plt.ylabel("Simulated Winning Bid")
plt.xlim(0, 450)
plt.ylim(0, 650)
plt.savefig(PLOT_DIRECTORY + EXPERIMENT_NAME + "win_v_start_sim.png")
plt.show()
plt.clf(); plt.cla()


# =====================================================================================================================
