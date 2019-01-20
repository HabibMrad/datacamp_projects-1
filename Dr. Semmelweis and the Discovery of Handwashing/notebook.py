# ## 1. Meet Dr. Ignaz Semmelweis

import pandas as pd

yearly = pd.read_csv('datasets/yearly_deaths_by_clinic.csv')
print(yearly)


# ## 2. The alarming number of deaths

# Calculate proportion of deaths per no. births
yearly['proportion_deaths'] = yearly.deaths / yearly.births

# Extract clinic 1 data into yearly1 and clinic 2 data into yearly2
yearly1 = yearly[yearly['clinic'] == 'clinic 1']
yearly2 = yearly[yearly['clinic'] == 'clinic 2']

print(yearly1)


# ## 3. Death at the clinics

# This makes plots appear in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# Plot yearly proportion of deaths at the two clinics
ax = yearly1.plot(x = 'year', y = 'proportion_deaths', label = 'yearly1' )
yearly2.plot(x = 'year', y = 'proportion_deaths', label = 'yearly2', ax = ax)
ax.set_ylabel('Proportion deaths')
#ax.show()


# ## 4. The handwashing begins

# Read datasets/monthly_deaths.csv into monthly
monthly = pd.read_csv('datasets/monthly_deaths.csv', parse_dates = True)
monthly['date'] = pd.to_datetime(monthly['date'])
# Calculate proportion of deaths per no. births
monthly['proportion_deaths'] = monthly.deaths / monthly.births
print(monthly.head(1))


# ## 5. The effect of handwashing

# Plot monthly proportion of deaths
ax = monthly.plot(x = 'date', y ='proportion_deaths')
ax.set_ylabel('Proportion deaths')


# ## 6. The effect of handwashing highlighted

# Date when handwashing was made mandatory
handwashing_start = pd.to_datetime('1847-06-01')

# Split monthly into before and after handwashing_start
before_washing = monthly[monthly['date'] < handwashing_start]
after_washing = monthly[monthly['date'] >= handwashing_start]

# Plot monthly proportion of deaths before and after handwashing
ax = before_washing.plot(x = 'date', y = 'proportion_deaths', label = 'before_washing')
after_washing.plot(x = 'date', y = 'proportion_deaths', label = 'after_washing', ax = ax)
ax.set_ylabel('Proportion deaths')


# ## 7. More handwashing, fewer deaths?

# Difference in mean monthly proportion of deaths due to handwashing
before_proportion = before_washing['proportion_deaths']
after_proportion = after_washing['proportion_deaths']
mean_diff = after_proportion.mean() - before_proportion.mean()
mean_diff


# ## 8. A Bootstrap analysis of Semmelweis handwashing data

# A bootstrap analysis of the reduction of deaths due to handwashing
boot_mean_diff = []

for i in range(3000):
    boot_before = before_proportion.sample(frac = 1, replace = True)
    boot_after = after_proportion.sample(frac = 1, replace = True)
    boot_mean_diff.append(boot_after.mean() - boot_before.mean())

# Calculating a 95% confidence interval from boot_mean_diff 
confidence_interval = pd.Series(boot_mean_diff).quantile([0.025, 0.975])
confidence_interval


# ## 9. The fate of Dr. Semmelweis

# The data Semmelweis collected points to that:
doctors_should_wash_their_hands = True

