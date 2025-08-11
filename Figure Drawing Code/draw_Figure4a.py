# Code to reproduce the overtime changes of APT victims
# This figure corresponds to Figure 4(a) in the paper 
# Section 4.1: Victim Countries

import pandas as pd
import numpy as np
import altair as alt

INPUT_CSV = '../Information_Retrieved_Collection.csv'
OUTPUT_PDF = 'Figure4a_VictimChanges.pdf'

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
Function to process the original data and filter to the victim countries
Enables to count the number of attacks per year for each victim country including zero-day attacks
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
    # Define Top 10 Victim Countries
    # ------------------------------
    top10_victim_countries = get_top_10(col, df)

    # Split 'Victims' on ','
    df[col] = df[col].apply(
        lambda x: [item.strip() for item in x.split(',')] if isinstance(x, str) else x
    )

    # Explode the Victims column
    df_exploded = df.explode(col)

    # Explicit copy
    df_filtered = df_exploded[df_exploded[col].isin(top10_victim_countries)].copy()

    # ------------------------------
    # Handle the 'Zero-day' Column
    # ------------------------------
    df_filtered['Zero-day'] = df_filtered['Zero-day'].astype(str).str.lower()

    # Set 'Zero-Day' to 1 if 'true', else 0
    df_filtered['Zero-day'] = np.where(df_filtered['Zero-day'] == 'true', 1, 0)

    # ------------------------------
    # Count Total Attacks and Zero-Day 
    # Attacks per Country per Year
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

    # Define custom size scale to include small values
    size_scale = alt.Scale(domain=[1, 10, 20, 30], range=[300, 800, 1300, 1800])

    # ------------------------------
    # Create the chart
    # ------------------------------
    chart = alt.Chart(df).mark_circle(opacity=0.8, stroke=None).encode(
        x=alt.X(
            "Country:N",
            sort=actor_order.tolist(),
            axis=alt.Axis(
                title="Victim Country",
                labelAngle=0,
                labelFontSize=28,
                titleFontSize=30,
                labelFontWeight="bold",
                titlePadding=110
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
                values=[1, 10, 20, 30],
                orient="none",
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
    print(f"[✓] Figure 4(a) saved to {OUTPUT_PDF}")
    
if __name__ == "__main__":
    final_df = process_filter_data(INPUT_CSV, 'Victim_country')
    draw_figure(final_df)