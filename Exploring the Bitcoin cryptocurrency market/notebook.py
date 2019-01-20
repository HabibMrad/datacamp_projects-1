
# ## 1. Bitcoin. Cryptocurrencies. So hot right now.

import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")
plt.style.use('fivethirtyeight')

# Reading in current data from coinmarketcap.com
current = pd.read_json("https://api.coinmarketcap.com/v1/ticker/")
print(current.head())


# ## 2. Full dataset, filtering, and reproducibility
dec6 = pd.read_csv('datasets/coinmarketcap_06122017.csv')

# Selecting the 'id' and the 'market_cap_usd' columns
market_cap_raw = dec6[['id', 'market_cap_usd']]
print(market_cap_raw.count())

# ## 3. Discard the cryptocurrencies without a market capitalization

# Filtering out rows without a market capitalization
cap = market_cap_raw.query('market_cap_usd > 0')
print(cap.count())

# ## 4. How big is Bitcoin compared with the rest of the cryptocurrencies?

#Declaring these now for later use in the plots
TOP_CAP_TITLE = 'Top 10 market capitalization'
TOP_CAP_YLABEL = '% of total cap'

# Selecting the first 10 rows and setting the index
cap10 = cap[0:10].set_index('id')

# Calculating market_cap_perc
cap10 = cap10.assign(market_cap_perc = lambda x : x.market_cap_usd / cap.market_cap_usd.sum() * 100)

# Plotting the barplot with the title defined above 
ax = cap10.plot.bar(y = 'market_cap_perc', title = TOP_CAP_TITLE)

# Annotating the y axis with the label defined above
ax.set_ylabel(TOP_CAP_YLABEL)

# ## 5. Making the plot easier to read and more informative

# Colors for the bar plot
COLORS = ['orange', 'green', 'orange', 'cyan', 'cyan', 'blue', 'silver', 'orange', 'red', 'green']

# Plotting market_cap_usd as before but adding the colors and scaling the y-axis  
ax = cap10.plot.bar(y = 'market_cap_usd', color = COLORS, title = TOP_CAP_TITLE)
ax.set_yscale('log')

# Annotating the y axis with 'USD'
ax.set_ylabel('USD')

# Final touch! Removing the xlabel as it is not very informative
ax.set_xlabel('')

# ## 6. What is going on?! Volatility in cryptocurrencies

# Selecting the id, percent_change_24h and percent_change_7d columns
volatility = dec6[['id', 'percent_change_24h', 'percent_change_7d']]

# Setting the index to 'id' and dropping all NaN rows
volatility = volatility.set_index('id').dropna(how = 'all')

# Sorting the DataFrame by percent_change_24h in ascending order
volatility = volatility.sort_values(by ='percent_change_24h')
print(volatility.head())

# ## 7. Well, we can already see that things are *a bit* crazy

#Defining a function with 2 parameters, the series to plot and the title
def top10_subplot(volatility_series, title):
    # Making the subplot and the figure for two side by side plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    
    # Plotting with pandas the barchart for the top 10 losers
    ax = volatility_series[:10].plot.bar(color = 'darkred', ax = axes[0])

    # Setting the figure's main title to the text passed as parameter
    fig.suptitle(title)
    
    # Setting the ylabel to '% change'
    ax.set_ylabel(TOP_CAP_YLABEL)
    
    # Same as above, but for the top 10 winners
    ax = volatility_series[-10:].plot.bar(color = 'darkblue', ax = axes[1])

    # Returning this for good practice, might use later
    return fig, ax

DTITLE = "24 hours top losers and winners"
volatility.dropna(subset =['percent_change_24h'], how = 'any', inplace = True)
print(volatility.tail())

# Calling the function above with the 24 hours period series and title DTITLE  
fig, ax = top10_subplot(volatility.percent_change_24h, DTITLE)

# ## 8. Ok, those are... interesting. Let's check the weekly Series too.

# Sorting in ascending order
volatility7d = volatility.sort_values(by = 'percent_change_7d', ascending=True)
volatility7d.dropna(subset =['percent_change_7d'], how = 'any', inplace = True)

WTITLE = "Weekly top losers and winners"

# Calling the top10_subplot function
fig, ax = top10_subplot(volatility7d.percent_change_7d, WTITLE)

# ## 9. How small is small?

# Selecting everything bigger than 10 billion 

#cap.dropna(subset=['market_cap_usd'], how = 'any', inplace = True)
largecaps = cap.query('market_cap_usd >  10000000000')
print(largecaps)

# ## 10. Most coins are tiny

# Making a nice function for counting different marketcaps from the
# "cap" DataFrame. Returns an int.

def capcount(query_string):
    return cap.query(query_string).count().id

# Labels for the plot
LABELS = ["biggish", "micro", "nano"]

# Using capcount count the biggish cryptos
biggish = capcount('market_cap_usd > 300000000')

# Same as above for micro ...
micro = capcount('market_cap_usd >= 50000000 & market_cap_usd < 300000000')

# ... and for nano
nano =  capcount('market_cap_usd < 50000000')

# Making a list with the 3 counts

values = [biggish,micro, nano]

import matplotlib.pyplot as plt
plt.bar(x = LABELS, height = values)

