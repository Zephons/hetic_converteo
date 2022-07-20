import pandas as pd
import numpy as np
import plotly.express as px
from plotly.graph_objs._figure import Figure
from datetime import date
from sqlalchemy import engine


def get_metrics_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> np.ndarray:
    sql_metrics = f"""
        SELECT SUM("Number of Comments")::TEXT AS "Sum Comments", SUM("Number of Ratings")::TEXT AS "Sum Ratings", ROUND(AVG("Average Rating")::NUMERIC, 2) AS "Aggregated Average Rating" FROM public.metrics_map WHERE "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}';
    """
    df_metrics = pd.read_sql_query(sql_metrics, engine)
    metrics_global = df_metrics.values[0]
    return metrics_global

def get_pie_chart_sentiment_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_pie_chart_sentiment = f"""
        SELECT "Sentiment", SUM("Count") AS "Sum" FROM public.pie_chart_sentiment WHERE "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}' GROUP BY "Sentiment";
    """
    df_pie_chart_sentiment = pd.read_sql_query(sql_pie_chart_sentiment, engine)
    pie_chart_sentiment_global = px.pie(
        names=df_pie_chart_sentiment["Sentiment"],
        values=df_pie_chart_sentiment["Sum"],
        title='Sentiment des avis',
        color=df_pie_chart_sentiment["Sentiment"],
        color_discrete_map={
            "Négatif": "#EF553B",
            "Positif": "#00CC96",
            "Neutre": "#636EFA"})
    pie_chart_sentiment_global.update_traces(textinfo="percent+label")
    pie_chart_sentiment_global.update_layout(
        autosize=False,
        width=400,
        height=400,
        font={"size": 15},
        title_x=0.5,
        showlegend=False)
    return pie_chart_sentiment_global

def get_map_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_map = f"""
    SELECT "City", "Address Without Number", "Latitude", "Longitude", SUM("Number of Ratings") AS "Number of Ratings", ROUND(AVG("Average Rating")::NUMERIC, 2) AS "Average Rating" FROM public.metrics_map WHERE "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}' GROUP BY "City", "Address Without Number", "Latitude", "Longitude";
    """
    df_map = pd.read_sql_query(sql_map, engine)
    px.set_mapbox_access_token("pk.eyJ1IjoidHplcGhvbnMiLCJhIjoiY2w1cXcwbHBtMjFrMTNwcGE5OTB3bGE0NCJ9.e5LRf5icKvgz-UkD4055fQ")
    map_global = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        color="Average Rating",
        hover_name="City",
        hover_data=["Number of Ratings", "Average Rating"],
        size="Number of Ratings",
        color_continuous_scale=px.colors.diverging.RdYlGn,
        opacity=0.8,
        size_max=30,
        mapbox_style="basic",
        zoom=5.1,
        width=1300,
        height=800)
    return map_global