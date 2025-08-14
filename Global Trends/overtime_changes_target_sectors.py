# Code to reproduce the overtime changes of APT target sectors
# This figure corresponds to Figure 5(a) in the paper 
# Section 4.1: Target Sectors

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

INPUT_CSV = '../Information_Retrieved_Collection.csv'
OUTPUT_PDF = 'Figure5a_TargetSectorChanges.pdf' 

'''
Function to process the original data and filter to the target sectors
Count the number of attacks per year for each target sector
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
    # Filter for the "Target_sector"
    # ------------------------------
    sector_df = df[df['Column'] == 'Target_sector'].reset_index(drop=True)
    sector_df['Subcategory'] = sector_df['Subcategory'].str.strip().str.title()

    target_sector_mapping = {
        'Government And Defense Agencies': 'Government/Defense',
        'Corporations And Businesses': 'Corporation/Business',
        'Financial Institutions': 'Financial',
        'Healthcare': 'Healthcare',
        'Energy And Utilities': 'Energy/Utility',
        'Cloud/Iot Services': 'Cloud/IoT',
        'Manufacturing': 'Manufacturing',
        'Education And Research Institutions': 'Education/Research',
        'Media And Entertainment Companies': 'Media/Entertainment',
        'Critical Infrastructure': 'Critical',
        'Non-Governmental Organizations (Ngos) And Nonprofits': 'NGO/Nonprofit',
        'Individuals': 'Individual'
    }
    sector_df['Subcategory'] = sector_df['Subcategory'].replace(target_sector_mapping)

    pivot_df = sector_df.pivot(index='Year', columns='Subcategory', values='Attacks').fillna(0)

    # ------------------------------
    # Reorder the columns to place 
    # the top 3 at the bottom
    # ------------------------------
    total_attacks = pivot_df.sum(axis=0).sort_values(ascending=False)
    top_three_sectors = total_attacks.head(3).index
    remaining_sectors = total_attacks.index.difference(top_three_sectors)
    ordered_columns = top_three_sectors.tolist() + remaining_sectors.tolist()
    pivot_df = pivot_df[ordered_columns]

    # ------------------------------
    # Set the color palette for each target sector
    # ------------------------------
    full_tab20 = sns.color_palette("tab20", 20)

    color_map = {
        'Government/Defense': full_tab20[0],
        'Corporation/Business': full_tab20[2],
        'Education/Research': full_tab20[4],
        'Cloud/IoT': full_tab20[5],
        'Critical': full_tab20[9],
        'Energy/Utility': full_tab20[8],
        'Financial': full_tab20[6],     
        'Healthcare': full_tab20[7],
        'Individual': full_tab20[10],
        'Manufacturing': full_tab20[11],
        'Media/Entertainment': full_tab20[14],
        'NGO/Nonprofit': full_tab20[15] 
    }

    colors = [color_map[sector] for sector in pivot_df.columns]

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
    plt.ylabel('Number of Target Sectors', fontsize=56, fontweight='bold')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.xticks(rotation=0, fontweight='bold')
    plt.yticks(ticks=range(0, 351, 50), fontweight='bold')

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
        
        # Determine top 3 sectors for this year
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
                    fontsize=40,
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
    print(f"[✓] Figure 5(a) saved to {OUTPUT_PDF}")

if __name__ == "__main__":
    final_df = process_filter_data(INPUT_CSV, 'Target_sector')
    draw_figure(final_df)