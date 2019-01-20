# ## 1. Winter is Coming. Let's load the dataset ASAP

import pandas as pd

book1 = pd.read_csv('datasets/book1.csv')
print(book1.head())

# ## 2. Time for some Network of Thrones
import networkx as nx

G_book1 = nx.Graph()


# ## 3. Populate the network with the DataFrame

for index, row in book1.iterrows():
    G_book1.add_edge(row['Source'], row['Target'], weight = row['weight'])

# Creating a list of networks for all the books
books = [G_book1]
book_fnames = ['datasets/book2.csv', 'datasets/book3.csv', 'datasets/book4.csv', 'datasets/book5.csv']
for book_fname in book_fnames:
    book = pd.read_csv(book_fname)
    G_book = nx.Graph()
    for _, edge in book.iterrows():
        G_book.add_edge(edge['Source'], edge['Target'], weight=edge['weight'])
    books.append(G_book)


# ## 4. Finding the most important character in Game of Thrones

# Calculating the degree centrality of book 1
deg_cen_book1 = nx.degree_centrality(books[0])

# Calculating the degree centrality of book 5
deg_cen_book5 = nx.degree_centrality(books[4])

# Sorting the dictionaries according to their degree centrality and storing the top 10
sorted_deg_cen_book1 = sorted(deg_cen_book1.items(), key = lambda x: x[1]*-1)[:9]

# Sorting the dictionaries according to their degree centrality and storing the top 10
sorted_deg_cen_book5 = sorted(deg_cen_book5.items(), key = lambda x: x[1]*-1)[:9]

# Printing out the top 10 of book1 and book5
print(sorted_deg_cen_book1, sorted_deg_cen_book5)


# ## 5. Evolution of importance of characters over the books

get_ipython().run_line_magic('matplotlib', 'inline')

# Creating a list of degree centrality of all the books
evol = [nx.degree_centrality(book) for book in books]

# Creating a DataFrame from the list of degree centralities in all the books
degree_evol_df = pd.DataFrame.from_records(evol)

# Plotting the degree centrality evolution of Eddard-Stark, Tyrion-Lannister and Jon-Snow
degree_evol_df.plot(y = ['Eddard-Stark', 'Tyrion-Lannister', 'Jon-Snow'])


# ## 6. What's up with Stannis Baratheon?

# Creating a list of betweenness centrality of all the books just like we did for degree centrality
evol = [nx.betweenness_centrality(book) for book in books]

# Making a DataFrame from the list
betweenness_evol_df = pd.DataFrame.from_records(evol).fillna(0)

# Finding the top 4 characters in every book
set_of_char = set()
for i in range(5):
    set_of_char |= set(list(betweenness_evol_df.T[i].sort_values(ascending=False)[0:4].index))
list_of_char = list(set_of_char)

# Plotting the evolution of the top characters
betweenness_evol_df.plot(y = list_of_char, figsize = (13, 7))


# ## 7. What does the Google PageRank algorithm tell us about Game of Thrones?

# Creating a list of pagerank of all the characters in all the books
evol = [nx.pagerank(book) for book in books]

# Making a DataFrame from the list
pagerank_evol_df = pd.DataFrame.from_records(evol)

# Finding the top 4 characters in every book
set_of_char = set()
for i in range(5):
    set_of_char |= set(list(pagerank_evol_df.T[i].sort_values(ascending=False)[0:4].index))
list_of_char = list(set_of_char)

# Plotting the top characters
pagerank_evol_df.plot(y = list_of_char, figsize = (13, 7))


# ## 8. Correlation between different measures

# Creating a list of pagerank, betweenness centrality, degree centrality
# of all the characters in the fifth book.
measures = [nx.pagerank(books[4]), 
            nx.betweenness_centrality(books[4], weight='weight'), 
            nx.degree_centrality(books[4])]

# Creating the correlation DataFrame
cor = pd.DataFrame.from_records(measures)

# Calculating the correlation
cor.T.corr()


# ## 9. Conclusion

# Finding the most important character in the fifth book,  
# according to degree centrality, betweenness centrality and pagerank.
p_rank, b_cent, d_cent = cor.loc[0].idxmax(0), cor.loc[1].idxmax(0), cor.loc[2].idxmax(0)

# Printing out the top character accoding to the three measures
print(p_rank, b_cent, d_cent)

