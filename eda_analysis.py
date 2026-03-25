"""
IPL Auction Value vs Performance Analyzer
Author: Somya Shrivastava
Tools: Python (Pandas, Matplotlib, Seaborn), SQL
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.titlesize': 13,
                     'axes.titleweight': 'bold', 'figure.facecolor': '#0D1117'})

# IPL colors
GOLD   = '#FFD700'; BLUE  = '#004BA0'; RED   = '#E03A3E'
GREEN  = '#00A86B'; WHITE = '#EEEEEE'; GRAY  = '#555555'
ORANGE = '#FF6B35'; PURPLE = '#6A0DAD'

df = pd.read_csv('ipl_auction_data.csv')
df_2024 = df[df['season'] == 2024]

print("="*60)
print("IPL AUCTION VALUE vs PERFORMANCE ANALYSIS")
print("="*60)
print(f"Total Records      : {len(df)}")
print(f"Seasons Covered    : {df['season'].nunique()} (2021–2024)")
print(f"Players Analyzed   : {df['player_name'].nunique()}")
print(f"Total Auction Spend: ₹{df_2024['auction_price_cr'].sum():.1f} Cr (2024)")
print(f"Overpaid Players   : {df_2024['overpaid'].sum()}")
print(f"Hidden Gems        : {df_2024['hidden_gem'].sum()}")

# ── Fig 1: Main Dashboard ────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.patch.set_facecolor('#0D1117')
fig.suptitle('🏏 IPL Auction Value vs Performance Dashboard (2021–2024)',
             fontsize=17, fontweight='bold', color=GOLD, y=1.01)
for ax in axes.flat:
    ax.set_facecolor('#161B22')
    ax.tick_params(colors=WHITE)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.title.set_color(GOLD)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRAY)

# 1. Scatter — Price vs Performance (2024) colored by Value
colors_scatter = [GREEN if v > 0.5 else RED if v < 0.15 else ORANGE
                  for v in df_2024['value_for_money']]
sc = axes[0,0].scatter(df_2024['auction_price_cr'], df_2024['performance_score'],
                        c=colors_scatter, s=80, alpha=0.85, edgecolors='white', linewidth=0.4)
axes[0,0].set_title('Price vs Performance (2024)')
axes[0,0].set_xlabel('Auction Price (₹ Cr)')
axes[0,0].set_ylabel('Performance Score')
green_p = mpatches.Patch(color=GREEN, label='Hidden Gem')
red_p   = mpatches.Patch(color=RED,   label='Overpaid')
org_p   = mpatches.Patch(color=ORANGE, label='Fair Value')
axes[0,0].legend(handles=[green_p, red_p, org_p], facecolor='#161B22',
                  labelcolor=WHITE, fontsize=8)

# Annotate top gems and overpaid
top_gems = df_2024.nlargest(3, 'value_for_money')
for _, row in top_gems.iterrows():
    axes[0,0].annotate(row['player_name'].split()[-1],
                        (row['auction_price_cr'], row['performance_score']),
                        textcoords="offset points", xytext=(5, 5),
                        fontsize=7, color=GREEN)

# 2. Team spending vs avg performance
team_stats = df_2024.groupby('team').agg(
    total_spend=('auction_price_cr', 'sum'),
    avg_perf=('performance_score', 'mean')
).reset_index().sort_values('total_spend', ascending=False)
bars = axes[0,1].bar(team_stats['team'], team_stats['total_spend'],
                      color=BLUE, edgecolor=GOLD, linewidth=0.5)
ax2 = axes[0,1].twinx()
ax2.plot(team_stats['team'], team_stats['avg_perf'], 'o-', color=GOLD,
          linewidth=2, markersize=6)
ax2.set_ylabel('Avg Performance Score', color=GOLD)
ax2.tick_params(colors=GOLD)
ax2.set_facecolor('#161B22')
axes[0,1].set_title('Team Spending vs Avg Performance')
axes[0,1].set_ylabel('Total Spend (₹ Cr)')
axes[0,1].tick_params(axis='x', rotation=45)

# 3. Role-wise value for money
role_vfm = df_2024.groupby('role')['value_for_money'].mean().sort_values(ascending=False)
role_colors = [GREEN, ORANGE, RED, BLUE][:len(role_vfm)]
axes[0,2].barh(role_vfm.index, role_vfm.values, color=role_colors, edgecolor='white')
axes[0,2].set_title('Avg Value-for-Money by Role')
axes[0,2].set_xlabel('Value for Money Score')
axes[0,2].axvline(role_vfm.mean(), color=GOLD, linestyle='--', label='Average')
axes[0,2].legend(facecolor='#161B22', labelcolor=WHITE, fontsize=8)
for i, v in enumerate(role_vfm.values):
    axes[0,2].text(v + 0.01, i, f'{v:.2f}', va='center', color=WHITE, fontsize=9)

# 4. Top 10 Hidden Gems
gems = df_2024.nlargest(10, 'value_for_money')[['player_name', 'auction_price_cr', 'value_for_money']]
bars_g = axes[1,0].barh(gems['player_name'], gems['value_for_money'], color=GREEN, edgecolor='white')
axes[1,0].set_title('🌟 Top 10 Hidden Gems (Best Value)')
axes[1,0].set_xlabel('Value for Money Score')
for i, (_, row) in enumerate(gems.iterrows()):
    axes[1,0].text(row['value_for_money'] + 0.01, i,
                    f"₹{row['auction_price_cr']}Cr", va='center', color=GOLD, fontsize=8)

# 5. Top 10 Overpaid
overpaid = df_2024.nsmallest(10, 'value_for_money')[['player_name', 'auction_price_cr', 'value_for_money']]
axes[1,1].barh(overpaid['player_name'], overpaid['auction_price_cr'], color=RED, edgecolor='white')
axes[1,1].set_title('💸 Most Overpaid Players')
axes[1,1].set_xlabel('Auction Price (₹ Cr)')
for i, (_, row) in enumerate(overpaid.iterrows()):
    axes[1,1].text(row['auction_price_cr'] + 0.1, i,
                    f"Score:{row['value_for_money']:.2f}", va='center', color=WHITE, fontsize=8)

# 6. Season-wise avg price trend by nationality
nat_season = df.groupby(['season', 'nationality'])['auction_price_cr'].mean().reset_index()
for nat in ['Indian', 'Australian', 'English', 'West Indian']:
    sub = nat_season[nat_season['nationality'] == nat]
    axes[1,2].plot(sub['season'], sub['auction_price_cr'], marker='o', label=nat, linewidth=2)
axes[1,2].set_title('Avg Auction Price Trend by Nationality')
axes[1,2].set_xlabel('Season')
axes[1,2].set_ylabel('Avg Price (₹ Cr)')
axes[1,2].legend(facecolor='#161B22', labelcolor=WHITE, fontsize=8)
axes[1,2].set_xticks([2021, 2022, 2023, 2024])

plt.tight_layout()
plt.savefig('ipl_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#0D1117')
plt.close()
print("\n✅ Dashboard saved: ipl_dashboard.png")

# ── Fig 2: Deep Dive ────────────────────────────────────────────
fig2, axes2 = plt.subplots(1, 3, figsize=(20, 6))
fig2.patch.set_facecolor('#0D1117')
fig2.suptitle('🔍 IPL Deep Dive — Statistical Analysis', fontsize=15, fontweight='bold', color=GOLD)
for ax in axes2:
    ax.set_facecolor('#161B22')
    ax.tick_params(colors=WHITE)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.title.set_color(GOLD)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRAY)

# Strike rate vs runs - batters
batters = df_2024[df_2024['role'].isin(['Batter', 'Wicket-Keeper'])]
sc2 = axes2[0].scatter(batters['runs_scored'], batters['strike_rate'],
                         c=batters['auction_price_cr'], cmap='YlOrRd', s=80, alpha=0.85)
plt.colorbar(sc2, ax=axes2[0], label='Auction Price (₹ Cr)')
axes2[0].set_title('Batters: Runs vs Strike Rate')
axes2[0].set_xlabel('Runs Scored')
axes2[0].set_ylabel('Strike Rate')

# Bowlers: wickets vs economy
bowlers = df_2024[df_2024['role'] == 'Bowler']
sc3 = axes2[1].scatter(bowlers['wickets'], bowlers['economy_rate'],
                         c=bowlers['auction_price_cr'], cmap='Blues', s=80, alpha=0.85)
plt.colorbar(sc3, ax=axes2[1], label='Auction Price (₹ Cr)')
axes2[1].set_title('Bowlers: Wickets vs Economy')
axes2[1].set_xlabel('Wickets')
axes2[1].set_ylabel('Economy Rate')

# Value for money distribution
axes2[2].hist(df_2024['value_for_money'], bins=20, color=GOLD, edgecolor='#0D1117', alpha=0.85)
axes2[2].axvline(df_2024['value_for_money'].mean(), color=GREEN, linestyle='--',
                  label=f"Mean: {df_2024['value_for_money'].mean():.2f}")
axes2[2].axvline(0.15, color=RED, linestyle=':', label='Overpaid threshold')
axes2[2].axvline(0.5, color=GREEN, linestyle=':', label='Hidden gem threshold')
axes2[2].set_title('Value-for-Money Distribution')
axes2[2].set_xlabel('Value for Money Score')
axes2[2].set_ylabel('Player Count')
axes2[2].legend(facecolor='#161B22', labelcolor=WHITE, fontsize=8)

plt.tight_layout()
plt.savefig('ipl_deep_dive.png', dpi=150, bbox_inches='tight', facecolor='#0D1117')
plt.close()
print("✅ Deep Dive saved: ipl_deep_dive.png")

# Key insights
print("\n" + "="*60)
print("KEY INSIGHTS (2024 Season)")
print("="*60)
top_gem = df_2024.loc[df_2024['value_for_money'].idxmax()]
most_overpaid = df_2024.loc[df_2024['value_for_money'].idxmin()]
top_spender = team_stats.iloc[0]
print(f"1. Best Value Player : {top_gem['player_name']} ({top_gem['team']}) — ₹{top_gem['auction_price_cr']}Cr")
print(f"2. Most Overpaid     : {most_overpaid['player_name']} ({most_overpaid['team']}) — ₹{most_overpaid['auction_price_cr']}Cr")
print(f"3. Biggest Spender   : {top_spender['team']} — ₹{top_spender['total_spend']:.1f}Cr total")
print(f"4. Overpaid Players  : {df_2024['overpaid'].sum()} out of {len(df_2024)}")
print(f"5. Hidden Gems Found : {df_2024['hidden_gem'].sum()} players under ₹5Cr with high performance")
print(f"6. Best Role Value   : {role_vfm.index[0]} — highest avg value for money")
print("\n✅ IPL Analysis Complete!")
