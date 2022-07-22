import pandas as pd
import numpy as np
import plotly.express as px
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
        SELECT "Sentiment", SUM("Count") AS "Sum" FROM public.pie_chart_sentiment WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}' GROUP BY "Sentiment";
    """
    df_pie_chart_sentiment = pd.read_sql_query(sql_pie_chart_sentiment, engine)
    pie_chart_sentiment_par_magasin = px.pie(
        names=df_pie_chart_sentiment["Sentiment"],
        values=df_pie_chart_sentiment["Sum"],
        title='Sentiment des avis',
        color=df_pie_chart_sentiment["Sentiment"],
        color_discrete_map={
            "Négatif": "#EF553B",
            "Positif": "#00CC96",
            "Neutre": "#636EFA"})
    pie_chart_sentiment_par_magasin.update_traces(textinfo="percent+label")
    pie_chart_sentiment_par_magasin.update_layout(
        autosize=False,
        width=400,
        height=400,
        font={"size": 15},
        title_x=0.5,
        showlegend=False)
    return pie_chart_sentiment_par_magasin