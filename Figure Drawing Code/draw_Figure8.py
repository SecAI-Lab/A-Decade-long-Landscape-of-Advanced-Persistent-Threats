# Code to reproduce the heatmap of top 20 countries
# This figure corresponds to Figure 8 in the paper 
# Section 4.3: Two-sided Nature as Both Attacker and Victim and Self-directed APT Attacks

import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

INPUT_CSV = '../Information_Retrieved_Collection.csv'
OUTPUT_PDF = 'Figure8_Heatmap.pdf' 

'''
Function to process the original data and filter to the top 20 attacker countries
Counts the number of cases where a country is both an attacker and a victim
'''
def process_filter_data(input_csv):
    # ------------------------------
    # Load and Prepare Data
    # ------------------------------
    df = pd.read_csv(input_csv)
    
    df.replace('NaN', pd.NA, inplace=True)
    df = df.dropna(subset=['Threat_country'])
    df = df[df['Threat_country'].notna()]
    
    df['Threat_country'] = df['Threat_country'].apply(
        lambda x: ';'.join(sorted(set(
            [c.strip() for c in x.replace('; ', ';').split(';') if c and c != 'NaN']
            )))
        )
    
    # ------------------------------
    #  Generate Threat–Victim pairs
    # ------------------------------
    processed_data = []
    for _, row in df.iterrows():
        threat_countries = row['Threat_country'].split(';')
        victims = row['Victim_country'] if pd.notna(row['Victim_country']) and row['Victim_country'].strip() else ''
        
        if victims:
            victim_list = sorted(set([v.strip() for v in victims.split(',')]))
            for threat in threat_countries:
                if threat:
                    for victim in victim_list:
                        processed_data.append([threat, victim])
    
    new_df = pd.DataFrame(processed_data, columns=['Threat_country', 'Victim_country'])
    
    # Count occurrences
    new_df['Value'] = new_df.groupby(['Threat_country', 'Victim_country'])['Victim_country'].transform('count')
    new_df = new_df.drop_duplicates()
    
    # ------------------------------
    # Filter to top 20 countries
    # ------------------------------
    country_value_sum = new_df.groupby('Threat_country')['Value'].sum()
    
    top_20_countries = country_value_sum.nlargest(20).index.tolist()
    
    final_df = new_df[new_df['Threat_country'].isin(top_20_countries)]
    
    return final_df

# Function to draw the figure
def draw_figure(input_df):
    mpl.rcParams['font.family'] = 'Liberation Sans'

    # Rename columns
    df = input_df.rename(columns={
        "Threat_country": "AttackerCol",
        "Victim_country": "VictimCol",
        "Value": "FlowValue"
    })
    df['AttackerCol'] = df['AttackerCol'].astype(str)
    df['VictimCol'] = df['VictimCol'].astype(str)

    # Sort attacker list alphabetically
    all_attackers = sorted(df['AttackerCol'].dropna().unique(), key=str)

    # ------------------------------
    # Create a pivot table for the heatmap
    # ------------------------------
    data_pivot = df.pivot_table(
        index='AttackerCol',
        columns='VictimCol',
        values='FlowValue',
        aggfunc='sum',
        fill_value=0
    )
    data_pivot = data_pivot.reindex(index=all_attackers, columns=all_attackers, fill_value=0)

    # Define custom colormap: white (low) to red (high)
    cmap = LinearSegmentedColormap.from_list("white_red", ["white", "red"])

    # ------------------------------
    # Create the heatmap
    # ------------------------------
    plt.figure(figsize=(13, 13))
    ax = sns.heatmap(
        data_pivot,
        cmap=cmap,
        annot=True,
        fmt="d",
        linewidths=0,
        linecolor='black',
        vmin=0,
        annot_kws={"size": 16, "ha": "center", "va": "center", "fontweight": "bold"},
        cbar_kws={"label": "", "pad": 0.08}
    )

    # Set outer border visible and bold
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_linewidth(2)

    # ------------------------------
    # Set axis properties
    # ------------------------------
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=16, fontweight='bold')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=16, fontweight='bold')
    ax.set_xlabel('Victim Country', fontsize=22, fontweight='bold')
    ax.set_ylabel('Attacker Country', fontsize=22, fontweight='bold')

    ax.set_aspect('equal')

    # ------------------------------
    # Customize colorbar
    # ------------------------------
    cbar = ax.collections[0].colorbar
    cbar.ax.set_title('# of Cases', fontsize=18, weight='bold', loc='left')
    cbar.ax.set_ylabel(' ', fontsize=15, weight='bold')
    cbar.ax.set_position([0.75, 0.194, 0.03, 0.58])
    cbar.ax.tick_params(labelsize=19)

    # Save to PDF
    plt.savefig(OUTPUT_PDF, format='pdf')
    print(f"[✓] Figure 8 saved to {OUTPUT_PDF}")

if __name__ == "__main__":
    final_df = process_filter_data(INPUT_CSV)
    draw_figure(final_df)