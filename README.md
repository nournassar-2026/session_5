# Chess Game Analysis

## 📊 Project Overview
This project analyzes chess game data to uncover patterns in player behavior, game outcomes, and opening strategies. The analysis includes win rates, rating differences, game length distributions, and duplicate move sequence detection.

## 📁 Data Sources
- **Chess Games Dataset**: 
"https://drive.google.com/file/d/1eR3NZtwIC6ECN3vhtrynqmx8okG0twA7/view?usp=sharing"

- **Player Registry Dataset**: 
 "https://drive.google.com/file/d/1wCSAkGagMzWiToedLC3ZGo_lGf_laF-k/view?usp=sharing"

Data is loaded in data file.

##  Technologies Used
- Python 3.x
- Pandas (Data manipulation)
- Matplotlib & Seaborn (Visualization)

# Data Cleaning Steps
Removed duplicate rows

Handled missing values in critical columns

Created rating_diff column (white_rating - black_rating)

Flagged suspicious short games (is_suspicious)

Standardized country names (if applicable)

## 📂 Project Structure
chess-analysis/
├── data/
│ ├── raw/ # Raw data files
│ │ ├── chess_games.csv
│ │ └── player_registry.csv
│ └── processed/ # Cleaned data
│ ├── chess_games_clean.csv
│ 
├── output/ # Generated visualizations
│ ├── wins_by_color.png
│ ├── boxplot_turns_by_victory_status.png
│ └── white_rating_vs_turns_rated.png
├── requirements.txt # Python dependencies
└── README.md # Project documentation
## 🔍 Key Analyses Performed

### 1. Win Rate Analysis
- White win rate:  49.86% 
- Black win rate:  45.40% 
- Draw rate:       4.74%
### 2. Game Length Distribution
- Short games (< 15 turns)
- Medium games (16-70 turns)
- Long games (> 70 turns)

### 3.  Games flagged as suspicious (< 5 turns)? 
- 342
### 4. Opening Family Popularity
- Most popular when White wins: Sicilian Defense.  1173 wins
- Most popular when Black wins:  Sicilian Defense.  1273 wins


## 📈 Visualizations
| Plot | Description |
|------|-------------|
| `wins_by_color.png` | Bar chart of win counts by color |
| `boxplot_turns_by_victory_status.png` | Turn distribution by game ending |
| `white_rating_vs_turns_rated.png` | Rating vs game length scatter plot |


## 🚀 How to Run

 Install dependencies
py -m pip install -r requirements.txt
clean.py

# Acknowledgments
Chess game data source