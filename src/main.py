from preprocessing import load_and_clean_data
from visualization import (
    plot_global_cases_deaths,
    plot_global_spread_over_time,
    plot_continent_cases_deaths,
    plot_lockdowns_vs_cases,
    plot_global_vaccination_progress,
    plot_current_global_snapshot,
    plot_country_trends,
    plot_choropleth_maps_by_continent
)

from eda import (
    basic_overview,
    plot_top10_total_cases,
    plot_top10_total_deaths,
    plot_correlation_heatmap
)

df = load_and_clean_data("owid-covid-data.csv")
#print(df.head(5))
#print("Preprocessed column names:")
#print(df.columns.tolist())

basic_overview(df)
plot_top10_total_cases(df)
plot_top10_total_deaths(df)
plot_correlation_heatmap(df)

plot_global_spread_over_time(df)

plot_global_cases_deaths(df)

plot_continent_cases_deaths(df)

plot_lockdowns_vs_cases(df)

plot_global_vaccination_progress(df)

plot_current_global_snapshot(df)

plot_country_trends(df, "Canada") # Replace CANADA with any other country

plot_choropleth_maps_by_continent(
    df,
    selected_continents=["Asia", "Europe"], 
    selected_year_ranges=["2021-2022"]
)
