# Code to reproduce the CDF and histogram of APT campaign durations
# This figure corresponds to Figure 6 in the paper
# Section 4.3: APT Duration

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

INPUT_CSV = '../Information_Retrieved_Collection.csv'
OUTPUT_PDF = 'Figure6_AttackDurationCDF.pdf' 

'''
Function to process the original data and filter to the attack durations
Draws a histogram and CDF of the attack durations
'''
def process_data_and_draw(input_csv, col):
    # ------------------------------
    # Load and Prepare Data
    # ------------------------------
    df = pd.read_csv(input_csv)

    duration_df = df.loc[pd.notna(df[col]), col]

    # Sort durations for CDF
    sorted_durations = np.sort(duration_df)
    cdf = np.arange(1, len(sorted_durations) + 1) / len(sorted_durations)

    # ------------------------------
    # Create a figure with twin axes:
    # Histogram and CDF
    # ------------------------------
    fig, ax1 = plt.subplots(figsize=(8, 6), dpi=300)

    # Plot histogram with actual counts
    bin_edges = np.arange(start=sorted_durations.min(), stop=sorted_durations.max() + 200, step=200)
    counts, bins, patches = ax1.hist(sorted_durations, bins=bin_edges, alpha=1, color='lightgray', edgecolor='black', density=False, zorder=3)

    ax1.set_xticks(np.arange(start=0, stop=sorted_durations.max() + 200, step=200))
    ax1.set_xlabel('Duration (Days)', fontsize=20, fontweight='bold')
    ax1.set_ylabel('Number of Attacks', fontsize=20, fontweight='bold', color='black')

    # Create a second y-axis for the CDF
    ax2 = ax1.twinx()
    ax2.plot(sorted_durations, cdf, marker='.', linestyle='-', linewidth=3.5, color='gray', markersize=12)
    ax2.set_ylabel('CDF', fontsize=20, fontweight='bold', color='black')

    # ------------------------------
    # Set axis properties
    # ------------------------------
    ax1.tick_params(axis='y', labelcolor='black')
    ax2.tick_params(axis='y', labelcolor='black')

    plt.setp(ax1.get_xticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax1.get_yticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax2.get_yticklabels(), fontsize=18, fontweight='bold')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']

    ax1.patch.set_edgecolor('black')
    ax1.patch.set_linewidth(1)

    ax1.tick_params(labelsize=18)
    ax2.tick_params(labelsize=18)
    ax1.grid(True, linestyle='--', linewidth=1.2, zorder=0)
    ax1.set_axisbelow(True)

    # Set limits to remove unwanted gaps
    ax1.set_xlim(left=0, right=1800)
    ax1.set_ylim(top=140)

    yticks = ax1.get_yticks()
    new_yticks = [tick for tick in yticks if tick != 0]
    ax1.set_yticks(new_yticks)

    for spine in ax1.spines.values():
        spine.set_linewidth(1)
        spine.set_color('black')
    
    # Save the plot as a PDF
    plt.tight_layout()
    plt.savefig(OUTPUT_PDF, dpi=300)
    print(f"[✓] Figure 6 plot saved to {OUTPUT_PDF}")

if __name__ == '__main__':
    process_data_and_draw(INPUT_CSV, 'Attack_duration')