# Code to reproduce the overtime changes of APT attack vectors
# This figure corresponds to Figure 5(b) in the paper 
# Section 4.1: Initial Attack Vectors

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

INPUT_CSV = '../Information_Retrieved_Collection.csv'
OUTPUT_PDF = 'Figure5b_AttackVectorChanges.pdf'

'''
Function to process the original data and filter to the attack vectors
Counts the number of attacks per year for each attack vector
'''
def process_filter_data(input_csv, col):
    # ------------------------------
    # Load and Prepare Data
    # ------------------------------
    df = pd.read_csv(input_csv)
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = df['Date'].dt.year

    # ------------------------------
    # Process the column
    # ------------------------------
    results = []
    df_filtered = df.dropna(subset=[col]).copy()
    df_filtered[col] = df_filtered[col].str.split(', ')
    df_filtered[col] = df_filtered[col].apply(lambda items: [item.strip() for item in items])
    df_exploded = df_filtered.explode(col)
    
    grouped = df_exploded.groupby(['Year', col]).size().reset_index(name='Attacks')
    grouped['Column'] = col.replace(' ', '')
    grouped = grouped.rename(columns={col: 'Subcategory'})
    results.append(grouped)

    # Combine all results into a single DataFrame
    final_df = pd.concat(results, ignore_index=True)

    return final_df

# Function to draw the figure
def draw_figure(input_df):
    df = input_df

    # ------------------------------
    # Filter for the "Attack_vector"
    # ------------------------------
    vector_df = df[df['Column'] == 'Attack_vector'].reset_index(drop=True)
    vector_df['Subcategory'] = vector_df['Subcategory'].str.strip().str.title()

    attack_vectors_mapping = {
        'Exploit Vulnerability': 'Vulnerability Exploitation'
    }
    vector_df['Subcategory'] = vector_df['Subcategory'].replace(attack_vectors_mapping)

    pivot_df = vector_df.pivot(index='Year', columns='Subcategory', values='Attacks').fillna(0)

    # ------------------------------
    # Reorder the columns to place 
    # the top 3 at the bottom
    # ------------------------------
    total_attacks = pivot_df.sum(axis=0).sort_values(ascending=False)
    top_three_vectors = total_attacks.head(3).index
    remaining_vectors = total_attacks.index.difference(top_three_vectors)
    ordered_columns = top_three_vectors.tolist() + remaining_vectors.tolist()
    pivot_df = pivot_df[ordered_columns]

    # ------------------------------
    # Set the color palette for each attack vector
    # ------------------------------
    full_tab20 = sns.color_palette("tab20", 20)

    color_map = {
        'Malicious Documents': full_tab20[0],
        'Spear Phishing': full_tab20[2],
        'Vulnerability Exploitation': full_tab20[4],
        'Covert Channels': full_tab20[5],
        'Credential Reuse': full_tab20[9],
        'Drive-By Download': full_tab20[8],
        'Meta Data Monitoring': full_tab20[6],     
        'Phishing': full_tab20[7],
        'Removable Media': full_tab20[10],
        'Social Engineering': full_tab20[11],
        'Watering Hole': full_tab20[14],
        'Website Equipping': full_tab20[15] 
    }

    colors = [color_map[vector] for vector in pivot_df.columns]

    # ------------------------------
    # Create the stacked bar plot
    # ------------------------------
    pivot_df.plot(
        kind='bar',
        stacked=True,
        figsize=(30, 17),
        color=colors
    )

    plt.xlabel('Year', fontsize=56, fontweight='bold')
    plt.ylabel('Number of Attack Vectors', fontsize=56, fontweight='bold')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.xticks(rotation=0, fontweight='bold')
    plt.yticks(ticks=range(0, 251, 50), fontweight='bold')

    # Add a legend below the plot
    legend = plt.legend(
        bbox_to_anchor=(0.5, -0.4),
        loc='center',
        fontsize=45,
        frameon=False,
        ncol=3
    )
    for text in legend.get_texts():
        text.set_fontweight('bold')

    # Make axis lines more bold
    ax = plt.gca()

    attacks_per_year = pivot_df.sum(axis=1).tolist()

    # Loop through each bar (year)
    for i, (index, row) in enumerate(pivot_df.iterrows()):
        cumulative_bottom = 0  # Start at the bottom of the bar
        
        # Determine top 3 vectors for this year
        top3_this_year = row.sort_values(ascending=False).head(3).index

        for category in pivot_df.columns:
            height = row[category]
            if category in top3_this_year and height > 0:
                x_pos = i
                y_pos = cumulative_bottom + height / 2

                ax.text(
                    x_pos,
                    y_pos,
                    f"{(height / attacks_per_year[i]) * 100:.0f}%",
                    ha='center',
                    va='center',
                    fontsize=42,
                    fontweight='bold',
                    color='white'
                )
            cumulative_bottom += height

    for spine in ax.spines.values():
        spine.set_linewidth(3)  
        spine.set_color('black')

    ax.tick_params(
        axis='both',
        length=10,
        width=2,
        pad=10,
        labelsize=52,
        direction='out'
    )

    # Grid and spines
    ax.set_axisbelow(True)
    ax.grid(True, linestyle='--', axis='y', linewidth=3)
    ax.xaxis.grid(False)

    # Add bold black border to entire plot
    ax.patch.set_edgecolor('black')
    ax.set_axisbelow(True)

    # Save the plot as a PDF
    plt.tight_layout()
    plt.savefig(OUTPUT_PDF, format='pdf')
    print(f"[✓] Figure 5(b) saved to {OUTPUT_PDF}")

if __name__ == "__main__":
    final_df = process_filter_data(INPUT_CSV, 'Attack_vector')
    draw_figure(final_df)