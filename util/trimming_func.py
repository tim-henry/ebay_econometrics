def trim_start_prices(start_prices, k):
    bids = np.array(start_prices)
    std = np.std(start_prices)
    median = np.median(start_prices)
    upper = median + std*k
    lower = median - std*k
    start_prices = start_prices[np.logical_and(start_prices>lower,start_prices<upper)]
    indexs = np.logical_and(start_prices>lower,start_prices<upper)
    return indexs, start_prices
    