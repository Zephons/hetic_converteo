import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs._figure import Figure
from datetime import date
from sqlalchemy import engine


def get_metrics_par_magasin(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> np.ndarray:
    sql_shop_info = f"""
        SELECT "Group Name", "Is Open" FROM public.shop_info WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$;
    """
    sql_metrics = f"""
        SELECT SUM("Number of Comments")::TEXT AS "Sum Comments", SUM("Number of Ratings")::TEXT AS "Sum Ratings", ROUND(AVG("Average Rating")::NUMERIC, 2) AS "Aggregated Average Rating" FROM public.metrics_map WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}';
    """
    df_shop_info = pd.read_sql_query(sql_shop_info, engine)
    df_metrics = pd.read_sql_query(sql_metrics, engine)
    metrics_par_magasin = np.append(df_shop_info.values[0], df_metrics.values[0])
    return metrics_par_magasin

def get_pie_chart_sentiment_par_magasin(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_pie_chart_sentiment = f"""
        SELECT "Sentiment", SUM("Count") AS "Sum" FROM public.sentiment WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}' GROUP BY "Sentiment";
    """
    df_pie_chart_sentiment = pd.read_sql_query(sql_pie_chart_sentiment, engine)
    pie_chart_sentiment_par_magasin = px.pie(
        data_frame=df_pie_chart_sentiment,
        names="Sentiment",
        values="Sum",
        category_orders={"Sentiment": ["Négatif", "Neutre", "Positif"]},
        color="Sentiment",
        color_discrete_map={
            "Négatif": "#EF553B",
            "Positif": "#00CC96",
            "Neutre": "#636EFA"})
    pie_chart_sentiment_par_magasin.update_layout(
        font={"size": 15},
        margin=dict(l=15, r=15, t=15, b=15),
        # legend=dict(
        #     yanchor="top",
        #     y=0.99,
        #     xanchor="left",
        #     x=0.005)
    )
    return pie_chart_sentiment_par_magasin

def get_bar_chart_good_topics_par_magasin(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_bar_chart_good_topics = f"""
        SELECT "main_word", SUM("Count") AS "Sum" FROM public.nmf_good WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}' GROUP BY "main_word" ORDER BY "Sum";
    """
    df_bar_chart_good_topics = pd.read_sql_query(sql_bar_chart_good_topics, engine)
    bar_chart_good_topics = go.Figure()
    bar_chart_good_topics.add_trace(go.Bar(
        y=df_bar_chart_good_topics["main_word"],
        x=df_bar_chart_good_topics["Sum"],
        name='Positif',
        orientation='h',
        marker=dict(
           color=df_bar_chart_good_topics['main_word'].value_counts().values,
           colorscale="Emrld",
           line=dict(color='rgba(38, 24, 74, 0.8)', width=1)
        )
    ))
    bar_chart_good_topics.update_layout(
        barmode='stack',
        font={"size": 15},
        xaxis=dict(
            showgrid=False,
            showline=False
        ),
        yaxis=dict(
            showgrid=False,
            showline=False
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=15, r=15, t=15, b=15))
    bar_chart_good_topics.update_xaxes(categoryorder='total ascending')
    return bar_chart_good_topics

def get_bar_chart_bad_topics_par_magasin(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_bar_chart_bad_topics = f"""
        SELECT "main_word", SUM("Count") AS "Sum" FROM public.nmf_bad WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}' GROUP BY "main_word" ORDER BY "Sum";
    """
    df_bar_chart_bad_topics = pd.read_sql_query(sql_bar_chart_bad_topics, engine)
    bar_chart_bad_topics = go.Figure()
    bar_chart_bad_topics.add_trace(go.Bar(
        y=df_bar_chart_bad_topics["main_word"],
        x=df_bar_chart_bad_topics["Sum"],
        name='Négatif',
        orientation='h',
        marker=dict(
           color=df_bar_chart_bad_topics['main_word'].value_counts().values,
           colorscale="ylorrd",
           line=dict(color='rgba(38, 24, 74, 0.8)', width=1)
        )
    ))
    bar_chart_bad_topics.update_layout(
        barmode='stack',
        font={"size": 15},
        xaxis=dict(
            showgrid=False,
            showline=False
        ),
        yaxis=dict(
            showgrid=False,
            showline=False
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=15, r=15, t=15, b=15))
    bar_chart_bad_topics.update_xaxes(categoryorder='total ascending')
    return bar_chart_bad_topics