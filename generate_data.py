import pandas as pd
import numpy as np

np.random.seed(42)

players = [
    ("Virat Kohli", "RCB", "Batter", "Indian"),
    ("Rohit Sharma", "MI", "Batter", "Indian"),
    ("MS Dhoni", "CSK", "Wicket-Keeper", "Indian"),
    ("Hardik Pandya", "MI", "All-Rounder", "Indian"),
    ("Jasprit Bumrah", "MI", "Bowler", "Indian"),
    ("KL Rahul", "LSG", "Batter", "Indian"),
    ("Ravindra Jadeja", "CSK", "All-Rounder", "Indian"),
    ("Shubman Gill", "GT", "Batter", "Indian"),
    ("Yuzvendra Chahal", "RR", "Bowler", "Indian"),
    ("Mohammed Siraj", "RCB", "Bowler", "Indian"),
    ("Pat Cummins", "SRH", "Bowler", "Australian"),
    ("Jos Buttler", "RR", "Batter", "English"),
    ("David Warner", "DC", "Batter", "Australian"),
    ("Faf du Plessis", "RCB", "Batter", "South African"),
    ("Quinton de Kock", "LSG", "Wicket-Keeper", "South African"),
    ("Glenn Maxwell", "RCB", "All-Rounder", "Australian"),
    ("Mitchell Starc", "KKR", "Bowler", "Australian"),
    ("Sunil Narine", "KKR", "All-Rounder", "West Indian"),
    ("Andre Russell", "KKR", "All-Rounder", "West Indian"),
    ("Nicholas Pooran", "LSG", "Wicket-Keeper", "West Indian"),
    ("Rashid Khan", "GT", "Bowler", "Afghan"),
    ("Mohammad Nabi", "SRH", "All-Rounder", "Afghan"),
    ("Trent Boult", "MI", "Bowler", "New Zealander"),
    ("Devon Conway", "CSK", "Batter", "New Zealander"),
    ("Liam Livingstone", "PBKS", "All-Rounder", "English"),
    ("Sam Curran", "PBKS", "All-Rounder", "English"),
    ("Ben Stokes", "CSK", "All-Rounder", "English"),
    ("Kagiso Rabada", "PBKS", "Bowler", "South African"),
    ("Anrich Nortje", "DC", "Bowler", "South African"),
    ("Sanju Samson", "RR", "Wicket-Keeper", "Indian"),
    ("Shreyas Iyer", "KKR", "Batter", "Indian"),
    ("Rishabh Pant", "DC", "Wicket-Keeper", "Indian"),
    ("Axar Patel", "DC", "All-Rounder", "Indian"),
    ("Washington Sundar", "SRH", "All-Rounder", "Indian"),
    ("Avesh Khan", "LSG", "Bowler", "Indian"),
    ("Arshdeep Singh", "PBKS", "Bowler", "Indian"),
    ("Umran Malik", "SRH", "Bowler", "Indian"),
    ("Ishan Kishan", "MI", "Wicket-Keeper", "Indian"),
    ("Prithvi Shaw", "DC", "Batter", "Indian"),
    ("Ruturaj Gaikwad", "CSK", "Batter", "Indian"),
    ("Tilak Varma", "MI", "Batter", "Indian"),
    ("Rinku Singh", "KKR", "Batter", "Indian"),
    ("Yashasvi Jaiswal", "RR", "Batter", "Indian"),
    ("Kuldeep Yadav", "DC", "Bowler", "Indian"),
    ("Deepak Chahar", "CSK", "Bowler", "Indian"),
    ("Shardul Thakur", "KKR", "All-Rounder", "Indian"),
    ("Harshal Patel", "RCB", "Bowler", "Indian"),
    ("T Natarajan", "SRH", "Bowler", "Indian"),
    ("Mohit Sharma", "GT", "Bowler", "Indian"),
    ("Shivam Dube", "CSK", "All-Rounder", "Indian"),
]

seasons = [2021, 2022, 2023, 2024]
records = []

for season in seasons:
    for player, team, role, nationality in players:
        matches = np.random.randint(8, 16)
        
        if role in ["Batter", "Wicket-Keeper"]:
            runs = np.random.randint(150, 700)
            avg = round(runs / np.random.randint(8, 15), 2)
            sr = round(np.random.uniform(120, 185), 2)
            fifties = np.random.randint(0, 5)
            hundreds = np.random.randint(0, 2)
            wickets = 0
            economy = 0
            bowling_avg = 0
        elif role == "Bowler":
            runs = np.random.randint(0, 80)
            avg = round(runs / np.random.randint(4, 12), 2)
            sr = round(np.random.uniform(80, 130), 2)
            fifties = 0
            hundreds = 0
            wickets = np.random.randint(8, 28)
            economy = round(np.random.uniform(6.5, 10.5), 2)
            bowling_avg = round(np.random.uniform(15, 35), 2)
        else:  # All-Rounder
            runs = np.random.randint(100, 450)
            avg = round(runs / np.random.randint(6, 14), 2)
            sr = round(np.random.uniform(130, 175), 2)
            fifties = np.random.randint(0, 4)
            hundreds = 0
            wickets = np.random.randint(5, 20)
            economy = round(np.random.uniform(7.0, 10.0), 2)
            bowling_avg = round(np.random.uniform(18, 38), 2)

        # Auction price (crores) - based on reputation + some noise
        star_players = ["Virat Kohli", "Rohit Sharma", "MS Dhoni", "Jasprit Bumrah",
                        "Mitchell Starc", "Pat Cummins", "Ben Stokes", "Sam Curran"]
        if player in star_players:
            auction_price = round(np.random.uniform(12, 24.75), 2)
        elif nationality != "Indian":
            auction_price = round(np.random.uniform(4, 14), 2)
        else:
            auction_price = round(np.random.uniform(0.5, 10), 2)

        # Performance score (composite)
        if role in ["Batter", "Wicket-Keeper"]:
            perf_score = round((runs/100) * 0.4 + (sr/150) * 0.3 + fifties * 0.2 + hundreds * 0.5 + matches * 0.02, 2)
        elif role == "Bowler":
            perf_score = round((wickets/10) * 0.5 + (10/economy if economy > 0 else 0) * 0.3 + matches * 0.02, 2)
        else:
            perf_score = round((runs/100) * 0.25 + (sr/150) * 0.2 + (wickets/10) * 0.3 + matches * 0.02, 2)

        value_for_money = round(perf_score / auction_price, 3)

        records.append({
            "season": season,
            "player_name": player,
            "team": team,
            "role": role,
            "nationality": nationality,
            "matches_played": matches,
            "runs_scored": runs,
            "batting_avg": avg,
            "strike_rate": sr,
            "fifties": fifties,
            "hundreds": hundreds,
            "wickets": wickets,
            "economy_rate": economy,
            "bowling_avg": bowling_avg,
            "auction_price_cr": auction_price,
            "performance_score": perf_score,
            "value_for_money": value_for_money,
            "overpaid": 1 if value_for_money < 0.15 else 0,
            "hidden_gem": 1 if value_for_money > 0.5 and auction_price < 5 else 0
        })

df = pd.DataFrame(records)
df.to_csv("ipl_auction_data.csv", index=False)
print(f"Dataset: {len(df)} records across {len(seasons)} seasons")
print(df.head())
