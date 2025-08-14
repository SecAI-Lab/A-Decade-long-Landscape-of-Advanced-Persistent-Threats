# Code to reproduce the overtime changes of APT threat actors
# This figure corresponds to Figure 4(b) in the paper 
# Section 4.1: Threat Actors

import pandas as pd
import numpy as np
import altair as alt

INPUT_CSV = '../Information_Retrieved_Collection.csv'
OUTPUT_PDF = 'Figure4b_ActorChanges.pdf'

# Helper function to get the top 10 most common items from the specified column
def get_top_10(column, df):
    df = df.dropna(subset=[column]).copy()
    df[column] = df[column].apply(lambda x: [v.strip() for v in str(x).split(',')])
    s = df.explode(column)[column]

    counts = (
        s.value_counts(dropna=False)
         .rename('Attacks')
         .to_frame()
         .reset_index()
         .rename(columns={'index': column})
         .sort_values(['Attacks', column], ascending=[False, True], kind='mergesort')
    )
    
    return counts.head(10)[column].tolist()

'''
Function to process the original data and filter to the  threat actors
Enables to count the number of attacks per year for each threat actor including zero-day attacks
'''
def process_filter_data(input_csv, col):
    # ------------------------------
    # Load and Prepare Data
    # ------------------------------
    df = pd.read_csv(input_csv)

    # Drop rows with missing 'Date' or 'Victims'
    df = df.dropna(subset=['Date', col])

    # Convert 'Date' to datetime format and extract the year
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = df['Date'].dt.year

    # ------------------------------
    # Define Top 10 Threat Actors
    # ------------------------------
    top10_threat_actors = get_top_10(col, df)

    # Split 'Threat Actor' on ','
    df[col] = df[col].apply(
        lambda x: [item.strip() for item in x.split(',')] if isinstance(x, str) else x
    )

    # Explode the Threat Actor column
    df_exploded = df.explode(col)

    # Explicit copy to avoid SettingWithCopyWarning
    df_filtered = df_exploded[df_exploded[col].isin(top10_threat_actors)].copy()
    
    # ------------------------------
    # Change Threat Actor Names
    # ------------------------------
    name_mapping = {
        "apt28": "APT28", "apt41": "APT41", "apt29": "APT29", "turla": "Turla",
        "apt34": "APT34", "fin7": "FIN7", "apt10": "APT10", "muddywater": "Muddywater",
        "sandworm": "Sandworm", "lazarus group": "Lazarus"
    }
    df_filtered[col] = df_filtered[col].map(name_mapping)

    # ------------------------------
    # Handle the 'Zero-day' Column
    # ------------------------------
    df_filtered['Zero-day'] = df_filtered['Zero-day'].astype(str).str.lower()

    # Set 'Zero-Day' to 1 if 'true', else 0
    df_filtered['Zero-day'] = np.where(df_filtered['Zero-day'] == 'true', 1, 0)

    # ------------------------------
    # Count Total Attacks and Zero-Day 
    # Attacks per Threat Actor per Year
    # ------------------------------
    final_df = (
        df_filtered.groupby(['Year', col])
        .agg(
            Attacks=(col, 'count'),   
            ZeroDayAttacks=('Zero-day', 'sum')
        )
        .reset_index()
        .rename(columns={col: 'Country'})
    )

    return final_df

# Function to draw the figure
def draw_figure(input_df):
    # Load your CSV file
    df = input_df

    # Calculate total number of attacks per threat actor
    actor_order = df.groupby("Country")["Attacks"].sum().sort_values(ascending=False).index

    # size_scale = alt.Scale(rangeMax=2000)
    size_scale = alt.Scale(domain=[1, 10, 20, 30], range=[300, 800, 1300, 1800])

    # ------------------------------
    # Create the chart
    # ------------------------------
    chart = alt.Chart(df).mark_circle(opacity=0.8, stroke=None).encode(
        x=alt.X(
            "Country:N",
            sort=actor_order.tolist(),
            axis=alt.Axis(
                title="Threat Actor",
                labelAngle=-45,
                labelFontSize=28,
                titleFontSize=30,
                labelFontWeight="bold"
            )
        ),
        y=alt.Y(
            "Year:N",
            axis=alt.Axis(
                title="Year",
                grid=False,
                labelFontSize=28,
                titleFontSize=30,
                labelFontWeight="bold"
            ),
            scale=alt.Scale(padding=1)
        ),
        size=alt.Size(
            "Attacks:Q",
            title="# of attacks",
            scale=size_scale,
            legend=alt.Legend(
                labelFontSize=24,
                titleFontSize=24,
                values=[1, 10, 20],
                orient='none',
                legendY = 270,
                legendX = 715
            )
        ),
        color=alt.Color(
            "ZeroDayAttacks:Q",
            scale=alt.Scale(scheme="reds", reverse=False),
            title="# of 0-days",
            legend=alt.Legend(
                labelFontSize=24,
                titleFontSize=24
            )
        )
    ).properties(
        width=700,
        height=500
    ).configure_view(
        strokeWidth=2,
        stroke="black"
    )

    # Save the chart as a PDF
    chart.save(OUTPUT_PDF)
    print(f"[✓] Figure 4(b) saved to {OUTPUT_PDF}")

if __name__ == "__main__":
    final_df = process_filter_data(INPUT_CSV, 'Threat_actor')
    draw_figure(final_df)