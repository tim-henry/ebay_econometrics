import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import analysis
import simulation

# =====================================================================================================================

EXPERIMENT_NAME = ""
DATA_DIRECTORY = "./auction_data/"
PLOT_DIRECTORY = "./plots/"
DISTRIBUTIONS = [
    st.dgamma, st.dweibull, st.cauchy, st.vonmises_line,
    st.alpha, st.anglit, st.betaprime, st.bradford, st.chi, st.cosine, st.exponnorm, st.f, st.foldnorm, st.genlogistic,
    st.genpareto, st.genexpon, st.gausshyper, st.genhalflogistic, st.gilbrat, st.gumbel_r, st.gumbel_l, st.halfcauchy,
    st.halflogistic, st.halfnorm, st.hypsecant, st.invgamma, st.invgauss, st.invweibull, st.johnsonsb, st.johnsonsu,
    st.ksone, st.kstwobign, st.logistic, st.loggamma, st.loglaplace, st.maxwell, st.mielke, st.nct, st.norm,
    st.powerlaw, st.reciprocal, st.rayleigh, st.rice, st.semicircular, st.t, st.triang, st.truncexpon, st.truncnorm,
    st.tukeylambda, st.uniform, st.wald, st.wrapcauchy
]

# ===============================================< ANALYSIS >===========================================================

# Get raw data
start_prices, winning_bids, winning_bid_auto = analysis.get_fraction_valid(DATA_DIRECTORY)
old_bids = np.array(analysis.get_all_bids(DATA_DIRECTORY))

# Extrapolate to bids below start price
bids = analysis.get_weighted_bids(old_bids, start_prices)

# Find best parametric distribution
best_bid_dist, best_bid_params = analysis.plot_best_dist(bids, "Bids", DISTRIBUTIONS, PLOT_DIRECTORY, EXPERIMENT_NAME)
analysis.plot_best_dist(start_prices, "Auction Start Price", DISTRIBUTIONS, PLOT_DIRECTORY, EXPERIMENT_NAME)
analysis.plot_best_dist(winning_bids, "Winning Bids", DISTRIBUTIONS, PLOT_DIRECTORY, EXPERIMENT_NAME)

# Plot winning bids
plt.hist(winning_bids, bins=range(int(np.min(winning_bids)), int(np.max(winning_bids)), 20), density=True)
plt.ylim(0, 0.03)
plt.title("Winning Bids")
plt.savefig(PLOT_DIRECTORY + EXPERIMENT_NAME + "winning_bid_dist_empirical.png")
plt.show()
plt.clf()
plt.cla()

# ==============================================< SIMULATION >==========================================================

# Generate auctions
n_bidders, n_auctions = 7, len(winning_bids)
first_price_prob = 1 - (np.sum(winning_bid_auto) / len(winning_bid_auto))
sim_start_prices, sim_winning_bids = simulation.generate_n_auctions(n_bidders, n_auctions, best_bid_dist,
                                                                    best_bid_params, start_prices)
simulation.plot_hist_of_sims(sim_winning_bids, range(int(np.min(winning_bids)), int(np.max(winning_bids)), 20),
                             PLOT_DIRECTORY, EXPERIMENT_NAME)

# Plot relationship between winning bids and start prices
plt.scatter(start_prices, winning_bids)
plt.title("Winning Bid v. Start Price (empirical)")
plt.xlabel("Start Price")
plt.ylabel("Winning Bid")
plt.xlim(0, 450)
plt.ylim(0, 650)
plt.savefig(PLOT_DIRECTORY + EXPERIMENT_NAME + "win_v_start_empirical.png")
plt.show()
plt.clf()
plt.cla()

# Plot simulated relationship between winning bids and start prices
plt.scatter(sim_start_prices, sim_winning_bids)
plt.title("Simulated Winning Bid v. Start Price")
plt.xlabel("Start Price")
plt.ylabel("Simulated Winning Bid")
plt.xlim(0, 450)
plt.ylim(0, 650)
plt.savefig(PLOT_DIRECTORY + EXPERIMENT_NAME + "win_v_start_sim.png")
plt.show()
plt.clf()
plt.cla()

# =====================================================================================================================
