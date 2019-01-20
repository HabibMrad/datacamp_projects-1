# ## 1. Introduction

# ## 2. Reading Data
import pandas as pd

colors = pd.read_csv('datasets/colors.csv')
colors.head()

# ## 3. Exploring Colors

# How many distinct colors are available?
num_colors = colors['name'].nunique()
print(num_colors)


# ## 4. Transparent Colors in Lego Sets

# colors_summary: Distribution of colors based on transparency
colors['is_trans'] = colors['is_trans'].astype('category')
colors_summary = colors.pivot_table(index='is_trans', aggfunc='count')
print(colors_summary)


# ## 5. Explore Lego Sets

get_ipython().run_line_magic('matplotlib', 'inline')
# Read sets data as `sets`
import matplotlib.pyplot as plt
sets = pd.read_csv('datasets/sets.csv')

# Create a summary of average number of parts by year: `parts_by_year`
parts_by_year = sets.pivot_table(index = 'year', aggfunc = 'mean').num_parts
# Plot trends in average number of parts by year
plt.plot(parts_by_year)


# ## 6. Lego Themes Over Years

# themes_by_year: Number of themes shipped by year
themes_by_year = sets[['year', 'theme_id']].groupby(by = 'year', as_index = False).
#themes_by_year = themes_by_year
print(themes_by_year)

