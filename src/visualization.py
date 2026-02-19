import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd

# Visualization 1: Global Spread Over Time

def plot_global_spread_over_time(df):
    # Filter only necessary columns
    df_map = df[['iso_code', 'location', 'date', 'total_cases']].copy()
    
    # Avoid errors from missing or zero-case entries
    df_map = df_map[df_map['total_cases'] > 0]

    # Plot animated choropleth map
    fig = px.choropleth(
        df_map,
        locations="iso_code",
        color="total_cases",
        hover_name="location",
        animation_frame=df_map["date"].dt.strftime('%Y-%m-%d'),
        color_continuous_scale="Reds",
        title="Global Spread of COVID-19 Over Time",
        labels={"total_cases": "Total Confirmed Cases"}
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        coloraxis_colorbar=dict(title="Cases")
    )

    fig.show()

# Visualization 2: Country specific trends over time

def plot_country_trends(df, country_name):

    country_df = df[df['location'] == country_name].copy()
    country_df['date'] = pd.to_datetime(country_df['date'])
    country_df.sort_values('date', inplace=True)

    # 7-day moving averages
    country_df['new_cases_ma'] = country_df['new_cases'].rolling(7).mean()
    country_df['new_deaths_ma'] = country_df['new_deaths'].rolling(7).mean()
    country_df['new_vaccinations_ma'] = country_df['new_vaccinations'].rolling(7).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(country_df['date'], country_df['new_cases_ma'], label='New Cases (7-day MA)', color='orange')
    plt.plot(country_df['date'], country_df['new_deaths_ma'], label='New Deaths (7-day MA)', color='red')
    plt.plot(country_df['date'], country_df['new_vaccinations_ma'], label='New Vaccinations (7-day MA)', color='green')

    plt.title(f"📈 COVID-19 Trends in {country_name}")
    plt.xlabel("Date")
    plt.ylabel("Count (7-day MA)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Visualization 3: Rise in Cases & Deaths (Multi-Line Chart)

def plot_global_cases_deaths(df):
    # Aggregate globally by date
    global_df = df.groupby('date')[['total_cases', 'total_deaths']].sum().reset_index()

    # Plot the lines
    plt.figure(figsize=(12, 6))
    plt.plot(global_df['date'], global_df['total_cases'], label='Total Cases', color='orange')
    plt.plot(global_df['date'], global_df['total_deaths'], label='Total Deaths', color='red')

    plt.xlabel("Date")
    plt.ylabel("Number of People")
    plt.title("Global COVID-19 Cases and Deaths Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Visualization 4: Choropleth Maps by Continent 

def plot_choropleth_maps_by_continent(df, selected_continents, selected_year_ranges):

    # Year range filter mapping
    year_filters = {
        "2020-2021": ("2020-01-01", "2021-01-01"),
        "2021-2022": ("2021-01-01", "2022-01-01"),
        "2022-2023": ("2022-01-01", "2023-01-01"),
        "2023-2024": ("2023-01-01", "2024-01-01"),
    }

    filtered = pd.DataFrame()
    for label in selected_year_ranges:
        start, end = pd.to_datetime(year_filters[label][0]), pd.to_datetime(year_filters[label][1])
        filtered = pd.concat([filtered, df[(df['date'] >= start) & (df['date'] < end)]])

    if filtered.empty:
        print("No data for selected year range(s).")
        return

    # Take latest record per country in selected continents
    latest_df = (
        filtered[filtered['continent'].isin(selected_continents)]
        .dropna(subset=['iso_code', 'total_cases', 'total_deaths', 'continent'])
        .sort_values('date')
        .groupby('location')
        .last()
        .reset_index()
    )

    # Choropleth for total cases
    fig_cases = px.choropleth(
        latest_df,
        locations="iso_code",
        color="total_cases",
        hover_name="location",
        color_continuous_scale="YlOrBr",
        title="🟡 Total COVID-19 Cases by Country",
        labels={"total_cases": "Total Cases"}
    )

    # Choropleth for total deaths
    fig_deaths = px.choropleth(
        latest_df,
        locations="iso_code",
        color="total_deaths",
        hover_name="location",
        color_continuous_scale="Reds",
        title="🔴 Total COVID-19 Deaths by Country",
        labels={"total_deaths": "Total Deaths"}
    )

    fig_cases.show()
    fig_deaths.show()

# Visualization 5: COVID-19 Cases & Deaths by Continent

def plot_continent_cases_deaths(df):
    # Drop rows without continent
    df = df.dropna(subset=['continent'])

    # Filter to rows that have total_cases or total_deaths > 0
    valid_rows = df[(df['total_cases'] > 0) | (df['total_deaths'] > 0)]

    # Find latest date with valid data
    latest_valid_date = valid_rows['date'].max()
    print("Using latest non-empty date:", latest_valid_date)

    latest_df = valid_rows[valid_rows['date'] == latest_valid_date]

    # Group by continent
    continent_df = latest_df.groupby('continent')[['total_cases', 'total_deaths']].sum().reset_index()
    
    # Plot stacked bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(continent_df['continent'], continent_df['total_cases'], label='Total Cases', color='skyblue')
    plt.bar(continent_df['continent'], continent_df['total_deaths'], label='Total Deaths',
            color='crimson', bottom=continent_df['total_cases'])

    plt.xlabel('Continent')
    plt.ylabel('Number of People')
    plt.title(f'Total COVID-19 Cases and Deaths by Continent\n(as of {latest_valid_date.date()})')
    plt.legend()
    plt.tight_layout()
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.show()

# Visualization 6: Lockdowns vs. Cases (Timeline Chart)

def plot_lockdowns_vs_cases(df):
    # Aggregate globally by date
    global_df = df.groupby('date')[['new_cases', 'stringency_index']].mean().reset_index()

    # Drop rows with missing stringency_index
    global_df = global_df.dropna(subset=['stringency_index'])

    # Plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Date')
    ax1.set_ylabel('New Cases', color='tab:red')
    ax1.plot(global_df['date'], global_df['new_cases'], color='tab:red', label='Daily New Cases')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    # Second Y-axis
    ax2 = ax1.twinx()
    ax2.set_ylabel('Stringency Index', color='tab:blue')
    ax2.plot(global_df['date'], global_df['stringency_index'], color='tab:blue', linestyle='--', label='Stringency Index')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    # Title and layout
    plt.title("Lockdowns vs. COVID-19 Case Surges (Global View)")
    fig.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.show()

# Visualization 7: Vaccination Progress Over Time

def plot_global_vaccination_progress(df):
    # Group by date, sum vaccinated columns
    vax_df = df.groupby('date')[['people_vaccinated', 'people_fully_vaccinated']].sum(min_count=1).reset_index()

    # Drop early dates where values are NaN
    vax_df = vax_df.dropna()

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(vax_df['date'], vax_df['people_vaccinated'], label='At least 1 dose', color='green')
    plt.plot(vax_df['date'], vax_df['people_fully_vaccinated'], label='Fully vaccinated', color='blue')

    plt.xlabel("Date")
    plt.ylabel("Number of People")
    plt.title("Global COVID-19 Vaccination Progress Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Visualization 8: “Where Are We Now?

def plot_current_global_snapshot(df):

    # Get the latest date
    latest_date = df['date'].max()
    latest_df = df[df['date'] == latest_date]

    # Drop rows with missing ISO codes or required columns
    latest_df = latest_df.dropna(subset=['iso_code', 'active_cases', 'people_fully_vaccinated_per_hundred'])

    # Build choropleth map
    fig = px.choropleth(
        latest_df,
        locations='iso_code',
        color='active_cases',
        hover_name='location',
        color_continuous_scale='Reds',
        title=f"🔥 Active COVID-19 Cases as of {latest_date.date()}",
        labels={'active_cases': 'Active Cases'}
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        coloraxis_colorbar=dict(title="Active Cases")
    )
    fig.show()

    # Now a second map for vaccination
    fig2 = px.choropleth(
        latest_df,
        locations='iso_code',
        color='people_fully_vaccinated_per_hundred',
        hover_name='location',
        color_continuous_scale='Greens',
        title=f"💉 Fully Vaccinated (% of Population) as of {latest_date.date()}",
        labels={'people_fully_vaccinated_per_hundred': '% Fully Vaccinated'}
    )

    fig2.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        coloraxis_colorbar=dict(title="% Vaccinated")
    )
    fig2.show()
