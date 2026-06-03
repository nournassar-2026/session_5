import pandas as pd
import os

def load_data(url, local_path):
    """Download from URL if not exists locally, else load from cache"""
    if os.path.exists(local_path):
        print(f'Loading from cache: {local_path}')
        return pd.read_csv(local_path)
    
    print(f'Downloading from {url}...')
    df = pd.read_csv(url)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    # Save to file
    df.to_csv(local_path, index=False)
    print(f'Saved to {local_path}')
    return df

#  URLs
url_1 = "https://drive.google.com/file/d/1eR3NZtwIC6ECN3vhtrynqmx8okG0twA7/view?usp=sharing"
url_2 = "https://drive.google.com/file/d/1wCSAkGagMzWiToedLC3ZGo_lGf_laF-k/view?usp=sharing"

# Create direct download URLs
url_1 = 'https://drive.google.com/uc?id=' + url_1.split('/')[-2]
url_2 = 'https://drive.google.com/uc?id=' + url_2.split('/')[-2]

# Load data with caching
df_chess = load_data(url_1, 'data/raw/chess_games.csv')
df_player_registry = load_data(url_2, 'data/raw/player_registry.csv')
# chess dataset
# 1-How many records are in the dataset?
print(f"\nChess games: {len(df_chess)} rows") # Chess games: 20058 rows

# showing examples
df_chess.head() 
# 2-How many exact duplicate rows exist?
duplicates_chess = df_chess.duplicated()
print(f"Number of duplicate rows in chess games: {duplicates_chess.sum()}") #Number of duplicate rows in chess games: 0
#3- How many games have duplicate move sequences?
# Only count duplicate games (excluding first occurrence)
extra_duplicates = df_chess.duplicated(subset=['moves'], keep='first').sum()
print(f"Extra duplicate game records: {extra_duplicates}") #Extra duplicate game records: 1138

#4-What % of opening_response is missing?
(df_chess['opening_response'].isna().mean() * 100)
print(f"{df_chess['opening_response'].isna().mean() * 100:.2f}%") #93.98%

# 5-What % of opening_variation is missing?
(df_chess['opening_variation'].isna().mean() * 100)
print(f"{df_chess['opening_variation'].isna().mean() * 100:.2f}%") #28.22%

#6-What is the minimum number of turns in any game? Why is this suspicious?
df_chess['turns'].min() # 1 , it is imposible to complete game in 1 turn

# Display null values per column for chess
print("\nNull values per column - Chess Games:")
print(df_chess.isnull().sum())
#Parse time_increment
df_chess[['time_base','time_inc']]=df_chess['time_increment'].str.split('+',expand=True).astype(int)
#Add rating_diff
df_chess['rating_diff']=df_chess['white_rating']-df_chess['black_rating']
print(df_chess[['white_rating', 'black_rating', 'rating_diff']].head(5))
#Q7: After adding rating_diff, what % of games did the higher-rated player win?
print(df_chess['winner'].unique()) # categories in winner col
non_draws = df_chess[df_chess['winner'] != 'Draw']
higher_wins_non_draws = ((non_draws['rating_diff'] > 0) & (non_draws['winner'] == 'White')) | \
                         ((non_draws['rating_diff'] < 0) & (non_draws['winner'] == 'Black'))

print(f"Higher-rated wins (excluding draws): {(higher_wins_non_draws.sum() / len(non_draws)) * 100:.1f}%")
#Higher-rated wins (excluding draws): 64.6%
#Q8: How many games are flagged as suspicious (< 5 turns)?
df_chess['is_suspicious']=df_chess['turns']<5 
df_chess['is_suspicious'].sum() # 342

#Q9: How many unique opening families exist?  
df_chess['opening_family']=df_chess['opening_fullname'].str.split(':').str[0].str.strip() #227
#  Drop opening_response because of high nulls
df_chess=df_chess.drop(columns=['opening_response'])
#Validate
assert df_chess['rating_diff'].notna().all()
assert df_chess.duplicated().sum() == 0
df_chess_clean =df_chess

print(f"\nCleaned data shapes:")
print(f"Chess games: {df_chess_clean.shape}")

# Save cleaned data to processed folder
os.makedirs('data/processed', exist_ok=True)

#Analytical Questions
#Q10 What is the win rate for White, Black, and Draw? (% of total games)
win_rates = df_chess['winner'].value_counts(normalize=True) * 100
for outcome, rate in win_rates.items():
    print(f"{outcome}: {rate:.2f}%") #White: 49.86%  Black: 45.40%  Draw: 4.74%
#Q11What is the most common way games end (victory_status)?
# With percentages
victory_status_pct = df_chess['victory_status'].value_counts(normalize=True) * 100
print(victory_status_pct.round(1).astype(str) + '%') #Resign 55.6% Mate 31.5% Out of Time 8.4% Draw  4.5%
most_common_end = df_chess['victory_status'].value_counts().index[0]
print(f"Most common: {most_common_end}") # Most common: Resign
#Q12 Which victory_status has the highest average number of turns?
# Group by victory_status and calculate mean turns
avg_turns_by_status = df_chess.groupby('victory_status')['turns'].mean()

# Find which one has the highest average
highest_avg_status = avg_turns_by_status.idxmax()
highest_avg_value = avg_turns_by_status.max()

print(f"{highest_avg_status}: {highest_avg_value:.1f} turns") # Draw: 83.8 turns
#Q 13 Which opening family is most popular when Black wins? Same for White?
most_popular_2 = df_chess[df_chess['winner'] == 'White']['opening_family'].value_counts().iloc[0:1]
print(f"most popular family when white wins: {most_popular_2.index[0]} ({most_popular_2.values[0]} games)")
#most popular family when black wins: Sicilian Defense (1273 games)
most_popular_2 = df_chess[df_chess['winner'] == 'White']['opening_family'].value_counts().iloc[0:1]
print(f"most popular family when white wins: {most_popular_2.index[0]} ({most_popular_2.values[0]} games)")
#most popular family when white wins: Sicilian Defense (1173 games)
#Q14 Do rated games have a different White win rate than unrated games? 
# Calculate white win rate for rated games
rated_games = df_chess[df_chess['rated'] == True]
rated_white_win = (rated_games['winner'] == 'White').sum() / len(rated_games) * 100

# Calculate white win rate for unrated games
unrated_games = df_chess[df_chess['rated'] == False]
unrated_white_win = (unrated_games['winner'] == 'White').sum() / len(unrated_games) * 100

print(f"Rated games: {rated_white_win:.1f}%")
print(f"Unrated games: {unrated_white_win:.2f}%")
# Rated games: 49.8%  Unrated games: 49.94%
# Q15 Classify each game as Short/Medium/Long using apply(). What % is each?
# Using apply() with a custom function / depends on threshold values
def classify_game(turns):
    if turns <= 15:
        return 'Short'
    elif turns <= 70:
        return 'Medium'
    else:
        return 'Long'

df_chess['game_length'] = df_chess['turns'].apply(classify_game)
percentages = df_chess['game_length'].value_counts(normalize=True) * 100
print(percentages.round(1).astype(str) + '%')
#Medium    62.2%  Long  32.0%   Short   5.8%