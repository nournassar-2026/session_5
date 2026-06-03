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


