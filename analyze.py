import pandas as pd
import matplotlib.pyplot as plt

# Project Objectives:
    # 1. WHAT TEAM IS THE MOST DOMINANT?
    # 2. WHICH TEAM HAS THE HIGHEST SCORE PER APPARATUS ON AVERAGE
    # 3. WHICH TEAM HAS SHOWN THE MOST IMPROVEMENT?
    # 4. WHICH TEAM IS THE MOST CONSISTENT?
    # 5. WHICH EVENT CORRELATES THE MOST WITH THE FINAL SCORE?

# Load the dataset
df = pd.read_csv("ncaa_gymnastics.csv")
#=========================================================================================================================
# |-------------------------|
# | DISPLAY WELCOME MESSAGE |
# |-------------------------|
print("========================================================")
print("    WELCOME TO THE NCAA GYMNASTICS ANALYSIS PROJECT!")
print("========================================================")
print()
print("This project aims to analyze the NCAA gymnastics dataset to answer the following questions:")
print("1. WHAT TEAM IS THE MOST DOMINANT?")
print("2. WHICH TEAM HAS THE HIGHEST SCORE PER APPARATUS ON AVERAGE?")
print("3. WHICH TEAM HAS SHOWN THE MOST IMPROVEMENT?")
print("4. WHICH TEAM IS THE MOST CONSISTENT?")
print("5. WHICH EVENT CORRELATES THE MOST WITH THE FINAL SCORE?")
print()
print("Let's dive into the analysis and uncover insights about NCAA gymnastics teams!")
print()
#=========================================================================================================================
# 1. WHAT TEAM IS THE MOST DOMINANT?

# |-----------------------------------------------------|
# | DOMINANT = MOST CHAMPIONSHIPS + MOST TOP 4 FINISHES |
# |-----------------------------------------------------|

# Utilize groupby or value_counts to determine which team has the highest number of championships and top 4 finishes

win = df[df['Rank'] == 1]
team_win = win['Team'].value_counts()

# Print the number of championships won by each team (descending)
print("=============[ TEAM CHAMPIONSHIP WINS ]=============")
print()
print(team_win.to_frame(name='Championships'))
print()

# Find count numbers for the top 4 finishes for each team
print("==============[ TEAM TOP 4 FINISHES ]===============")
top4 = df[df['Rank'] <= 4]
team_top4 = top4['Team'].value_counts()
# Print the top 4 finishes for each team (descending)
print()
print(team_top4.to_frame(name='Top 4 Finishes'))
print()

# Now group the teams by which team has the most championships and top 4 finishes. They are the most dominant team
dominant = team_win.add(team_top4, fill_value=0)
dominant = dominant.sort_values(ascending=False)
print("================[ TEAM DOMINANCE ]=================")
print()
print(dominant.to_frame(name='Dominance'))
print()

# Utilize a matplotlib bar chart to visualize the dominance of each team based on championships and top 4 finishes

# Select the top 10 teams
top_teams = dominant.head(10)

# Create the bar chart
plt.figure()
plt.bar(top_teams.index, top_teams.values, color='skyblue')

# Add labels and title
plt.xticks(rotation=45)
plt.xlabel('Team')
plt.ylabel('Combined Dominance Score')
plt.title('Top 10 NCAA Gymnastics Teams by Dominance')

plt.tight_layout()
plt.show()

#=========================================================================================================================
# 2. WHICH TEAM HAS THE HIGHEST SCORE PER APPARATUS ON AVERAGE
# Group the data by team and calculate the average score for each apparatus

average_scores = df.groupby('Team')[['Vault']].mean()
average_scores_vault = average_scores.sort_values(by=['Vault'], ascending=False)
average_scores = df.groupby('Team')[['Bars']].mean()
average_scores_bars = average_scores.sort_values(by=['Bars'], ascending=False)
average_scores = df.groupby('Team')[['Beam']].mean()
average_scores_beam = average_scores.sort_values(by=['Beam'], ascending=False)
average_scores = df.groupby('Team')[['Floor']].mean()
average_scores_floor = average_scores.sort_values(by=['Floor'], ascending=False)
print("=========[ AVERAGE SCORES PER APPARATUS ]==========")
print()
print(round(average_scores_vault, 3))
print()
print(round(average_scores_bars, 3))
print()
print(round(average_scores_beam, 3))
print()
print(round(average_scores_floor, 3))
print()

# Must do this for EVERY TEAM FOR EVERY YEAR to get the most accurate results, which we did do above
#=========================================================================================================================
# 3. WHICH TEAM HAS SHOWN THE MOST IMPROVEMENT?
# Find the average score for each team in the first three years and the last three years, then calculate the difference
# to determine which team has shown the most improvement

average = df.groupby(['Team', 'Year'])[['Vault', 'Bars', 'Beam', 'Floor']].mean()
first_three_years = average[average.index.get_level_values('Year') <= 2015].groupby('Team').mean()
last_three_years = average[average.index.get_level_values('Year') >= 2016].groupby('Team').mean()
improvement = last_three_years - first_three_years
improvement['Total Improvement'] = improvement.sum(axis=1)
improvement = improvement.sort_values(by='Total Improvement', ascending=False)
print("===============[ TEAM IMPROVEMENT ]================")
print()
print(round(improvement, 3))
print()
#=========================================================================================================================
# 4. WHICH TEAM IS THE MOST CONSISTENT?
# Calculate the standard deviation of the scores for each team. The team with the lowest standard deviation is the most consistent
# Only consider teams that have appeared 3 or more times to ensure a more accurate representation of consistency

appear = df['Team'].value_counts()
appearances = appear[appear >= 3].index
consistent_team = df[df['Team'].isin(appearances)]
consistency = consistent_team.groupby('Team')['Total'].std()
consistency = consistency.sort_values(ascending=True)
print("===============[ TEAM CONSISTENCY ]================")
print()
print("Only teams that appear 3 or more times are considered.")
print()
print(round(consistency.to_frame(name='Consistency'), 3))
print()
#=========================================================================================================================
# 5. WHICH EVENT CORRELATES THE MOST WITH THE FINAL SCORE?
# Calculate the correlation between each apparatus score and the total score. The apparatus with the highest correlation
# is the one that correlates the most with the final score

correlation = df[['Vault', 'Bars', 'Beam', 'Floor', 'Total']].corr()
correlation_with_total = correlation['Total'].drop('Total')
correlation_with_total = correlation_with_total.sort_values(ascending=False)
print("==========[ CORRELATION WITH FINAL SCORE ]==========")
print()
print(round(correlation_with_total.to_frame(name='Correlation'), 3))
print()
print("====================================================")
#=========================================================================================================================
