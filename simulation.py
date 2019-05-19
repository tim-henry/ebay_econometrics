import matplotlib.pyplot as plt
import numpy as np


def generate_n_samples(n, dist, params):
    samples = np.array(dist.rvs(*params, size=n * 5))
    return np.round(samples[samples >= 0][:n + 1])


def generate_auction(i, n_bidders, bid_dist, bid_params, start_prices, depth=0):
    start_price = start_prices[i]
    bids = sorted(generate_n_samples(n_bidders, bid_dist, bid_params))
    highest = bids[-1]
    if depth > 3:
        return start_price, bids, None
    if highest > start_price:
        return start_price, bids, highest
    else:
        return generate_auction(i, n_bidders, bid_dist, bid_params, start_prices, depth=depth + 1)


def generate_n_auctions(n_bidders, n_auctions, bid_dist, bid_params, start_prices):
    sim_start_prices = []
    sim_sale_prices = []
    for i in range(n_auctions):
        start_price, _, sale_price = generate_auction(i, n_bidders, bid_dist, bid_params, start_prices)
        sim_start_prices.append(start_price)
        sim_sale_prices.append(sale_price)
    return sim_start_prices, sim_sale_prices


def plot_hist_of_sims(sale_prices, plot_range, plot_directory, experiment_name):
    fig, ax = plt.subplots()
    sale_prices = np.array(sale_prices)
    sale_prices = sale_prices[sale_prices != np.array(None)]
    sale_prices = sale_prices.astype(int)
    ax.hist(sale_prices, bins=plot_range, density=True)
    plt.ylim(0, 0.03)
    plt.title("Simulated Winning Bids")
    plt.savefig(plot_directory + experiment_name + "winning_bid_dist_sim.png")
    plt.show()
    plt.clf();
    plt.cla()
