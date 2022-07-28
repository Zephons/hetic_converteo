import os
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.graph_objs._figure import Figure
from datetime import date
from sqlalchemy import engine


def get_metrics_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> np.ndarray:
    sql_shop_info = f"""
        SELECT "Is Open" FROM public.shop_info;
    """
    sql_metrics_global = f"""
        SELECT SUM("Number of Comments")::TEXT AS "Sum Comments", SUM("Number of Ratings")::TEXT AS "Sum Ratings", ROUND(SUM("Number of Comments") / COUNT(DISTINCT "Address Without Number"), 0)::TEXT AS "Sum Comments per Shop", ROUND(AVG("Average Rating")::NUMERIC, 2) AS "Aggregated Average Rating" FROM public.metrics_map WHERE "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}';
    """
    df_shop_info = pd.read_sql_query(sql_shop_info, engine)
    df_metrics = pd.read_sql_query(sql_metrics_global, engine)
    nb_shops_in_operation = sum(df_shop_info["Is Open"])
    nb_shops = len(df_shop_info)
    metrics_global = np.append((nb_shops_in_operation, nb_shops), df_metrics.values[0])
    return metrics_global

def get_pie_chart_sentiment_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_pie_chart_sentiment = f"""
        SELECT "Sentiment", SUM("Count") AS "Nombre de notes" FROM public.sentiment WHERE "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "Sentiment";
    """
    df_pie_chart_sentiment = pd.read_sql_query(sql_pie_chart_sentiment, engine)
    pie_chart_sentiment_global = px.pie(
        data_frame=df_pie_chart_sentiment,
        names="Sentiment",
        values="Nombre de notes",
        category_orders={"Sentiment": ["Négatif", "Neutre", "Positif"]},
        color="Sentiment",
        color_discrete_map={
            "Négatif": "#EF553B",
            "Positif": "#00CC96",
            "Neutre": "#636EFA"})
    pie_chart_sentiment_global.update_layout(
        font={"size": 15},
        margin=dict(l=15, r=15, t=15, b=15),
        # legend=dict(
        #     yanchor="top",
        #     y=0.99,
        #     xanchor="left",
        #     x=0.005)
    )
    return pie_chart_sentiment_global

def get_bar_chart_group_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_bar_chart_group = f"""
        SELECT "Group Name" AS "Group", "Sentiment", SUM("Count") AS "Nombre de notes" FROM public.sentiment WHERE "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "Group", "Sentiment" ORDER BY "Group", "Sentiment";
    """
    df_bar_chart_group_global = pd.read_sql_query(sql_bar_chart_group, engine)
    bar_chart_group_global = px.bar(
        data_frame=df_bar_chart_group_global,
        x="Group",
        y="Nombre de notes",
        color="Sentiment",
        color_discrete_map={
            "Négatif": "#EF553B",
            "Positif": "#00CC96",
            "Neutre": "#636EFA"})
    bar_chart_group_global.update_layout(
        font={"size": 15},
        margin=dict(l=15, r=15, t=15, b=15),
        xaxis_title=None,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return bar_chart_group_global

def get_map_global(engine: engine.base.Engine, secrets: dict, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_map = f"""
        SELECT "City", "Address Without Number", "Latitude", "Longitude", SUM("Number of Ratings") AS "Nombre de notes", ROUND(AVG("Average Rating")::NUMERIC, 2) AS "Note moyenne" FROM public.metrics_map WHERE "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "City", "Address Without Number", "Latitude", "Longitude";
    """
    df_map = pd.read_sql_query(sql_map, engine)
    mapbox_token = os.environ.get("MAPBOX_TOKEN") or secrets.get("MAPBOX").get("ACCESS_TOKEN")
    px.set_mapbox_access_token(mapbox_token)
    map_global = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        color="Note moyenne",
        hover_name="City",
        hover_data=["Nombre de notes", "Note moyenne"],
        size="Nombre de notes",
        color_continuous_scale=px.colors.diverging.RdYlGn,
        opacity=0.8,
        size_max=30,
        mapbox_style="basic",
        zoom=5.1,
        width=1300,
        height=700)
    map_global.update_layout(
        font={"size": 15},
        margin=dict(l=15, r=15, t=15, b=15)
    )
    return map_global

def get_bar_chart_good_topics_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_bar_chart_good_topics = f"""
        SELECT "Topic" AS "Sujet", SUM("Count") AS "Nombre d'avis" FROM public.nmf_good WHERE "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "Topic" ORDER BY "Topic" DESC;
    """
    df_bar_chart_good_topics = pd.read_sql_query(sql_bar_chart_good_topics, engine)
    bar_chart_good_topics = px.bar(
        data_frame=df_bar_chart_good_topics,
        x="Nombre d'avis",
        y="Sujet",
        color_discrete_sequence=["#00CC96"],
        orientation="h")
    bar_chart_good_topics.update_layout(
        font={"size": 15},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=15, b=15))
    return bar_chart_good_topics

def get_bar_chart_bad_topics_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_bar_chart_bad_topics = f"""
        SELECT "Topic" AS "Sujet", SUM("Count") AS "Nombre d'avis" FROM public.nmf_bad WHERE "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "Topic" ORDER BY "Topic" DESC;
    """
    df_bar_chart_bad_topics = pd.read_sql_query(sql_bar_chart_bad_topics, engine)
    bar_chart_bad_topics = px.bar(
        data_frame=df_bar_chart_bad_topics,
        x="Nombre d'avis",
        y="Sujet",
        color_discrete_sequence=["#EF553B"],
        orientation="h")
    bar_chart_bad_topics.update_layout(
        font={"size": 15},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=15, b=15))
    return bar_chart_bad_topics

def get_radar_chart_good_topics_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_radar_chart_good_topics = f"""
        SELECT "Topic" AS "Sujet", SUM("Count") AS "Nombre d'avis" FROM public.nmf_good WHERE "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "Topic" ORDER BY "Topic" DESC;
    """
    df_radar_chart_good_topics = pd.read_sql_query(sql_radar_chart_good_topics, engine)
    radar_chart_good_topics = px.line_polar(
        data_frame=df_radar_chart_good_topics,
        r="Nombre d'avis",
        theta="Sujet",
        color_discrete_sequence=["#00CC96"],
        line_close=True)
    radar_chart_good_topics.update_traces(
        fillcolor='#00CC96',
        fill="toself",
        # opacity=0.7
    )
    radar_chart_good_topics.update_layout(
        font={"size": 15},
        margin=dict(t=30, b=30)
    )
    return radar_chart_good_topics

def get_radar_chart_bad_topics_global(engine: engine.base.Engine, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_radar_chart_good_topics = f"""
        SELECT "Topic" AS "Sujet", SUM("Count") AS "Nombre d'avis" FROM public.nmf_bad WHERE "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "Topic" ORDER BY "Topic" DESC;
    """
    df_radar_chart_bad_topics = pd.read_sql_query(sql_radar_chart_good_topics, engine)
    radar_chart_bad_topics = px.line_polar(
        data_frame=df_radar_chart_bad_topics,
        r="Nombre d'avis",
        theta="Sujet",
        color_discrete_sequence=["#EF553B"],
        line_close=True)
    radar_chart_bad_topics.update_traces(
        fillcolor='#EF553B',
        fill="toself",
        # opacity=0.7
    )
    radar_chart_bad_topics.update_layout(
        font={"size": 15},
        margin=dict(t=30, b=30)
    )
    return radar_chart_bad_topics