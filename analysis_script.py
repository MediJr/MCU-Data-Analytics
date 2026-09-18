import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('marvel_movies_dataset.csv')

print("📊 Marvel Movies Dataset Analysis")
print("=" * 50)
print(f"Total Movies: {len(df)}")
print(f"Phases: {df['phase'].unique()}")
print(f"Date Range: {df['release_date'].min()} to {df['release_date'].max()}")

# Top 5 highest grossing movies
print("\n💰 Top 5 Highest Grossing Movies:")
top_5 = df.nlargest(5, 'worldwide_box_office_millions')[['movie_title', 'worldwide_box_office_millions', 'phase']]
print(top_5.to_string(index=False))

# Average ratings by phase
print("\n⭐ Average Ratings by Phase:")
phase_ratings = df.groupby('phase').agg({
    'imdb_rating': 'mean',
    'rotten_tomatoes': 'mean',
    'metacritic_score': 'mean'
}).round(2)
print(phase_ratings)

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Box Office by Phase
df.groupby('phase')['worldwide_box_office_millions'].sum().plot(kind='bar', ax=axes[0,0])
axes[0,0].set_title('Total Box Office by MCU Phase')
axes[0,0].set_ylabel('Worldwide Box Office (Millions)')

# 2. Ratings by Phase
df.groupby('phase')['imdb_rating'].mean().plot(kind='bar', ax=axes[0,1], color='green')
axes[0,1].set_title('Average IMDb Rating by Phase')
axes[0,1].set_ylabel('IMDb Rating')

# 3. Budget vs Box Office
df.plot(kind='scatter', x='production_budget_millions', 
        y='worldwide_box_office_millions', ax=axes[1,0])
axes[1,0].set_title('Budget vs Box Office')
axes[1,0].set_xlabel('Production Budget (Millions)')
axes[1,0].set_ylabel('Worldwide Box Office (Millions)')

# 4. Top 10 Movies by Profit
df.nlargest(10, 'profit_millions').plot(kind='bar', x='movie_title', 
                                        y='profit_millions', ax=axes[1,1])
axes[1,1].set_title('Top 10 Most Profitable Movies')
axes[1,1].set_ylabel('Profit (Millions)')
axes[1,1].set_xlabel('')

plt.tight_layout()
plt.savefig('marvel_movies_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ Analysis complete! Visualization saved as 'marvel_movies_analysis.png'")
