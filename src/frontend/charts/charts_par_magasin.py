import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
from plotly.graph_objs._figure import Figure
from datetime import date
from sqlalchemy import engine
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

from src.backend.methods import get_file_setting


file_setting = get_file_setting("settings.yml")

def get_metrics_par_magasin(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> np.ndarray:
    sql_shop_info = f"""
        SELECT "Group Name", "Is Open" FROM public.shop_info WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$;
    """
    sql_metrics_par_magasin = f"""
        SELECT SUM("Number of Comments") AS "Sum Comments", SUM("Number of Ratings") AS "Sum Ratings", AVG("Average Rating") AS "Aggregated Average Rating" FROM public.metrics_map WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}';
    """
    sql_metrics_global = f"""
        SELECT ROUND(SUM("Number of Comments") / COUNT(DISTINCT "Address Without Number"), 0) AS "Sum Comments per Shop", ROUND(SUM("Number of Ratings") / COUNT(DISTINCT "Address Without Number"), 0) AS "Sum Ratings per Shop", AVG("Average Rating") AS "Aggregated Average Rating" FROM public.metrics_map WHERE "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}';
    """
    df_shop_info = pd.read_sql_query(sql_shop_info, engine)
    df_metrics_par_magasin = pd.read_sql_query(sql_metrics_par_magasin, engine)
    df_metrics_global = pd.read_sql_query(sql_metrics_global, engine)
    metrics_par_magasin = df_metrics_par_magasin.values[0]
    metrics_global = df_metrics_global.values[0]
    metrics_difference = metrics_par_magasin - metrics_global
    metrics = np.append(df_shop_info.values[0], list(zip(metrics_par_magasin, metrics_difference)))
    return metrics

def get_pie_chart_sentiment_par_magasin(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_pie_chart_sentiment = f"""
        SELECT "Sentiment", SUM("Count") AS "Nombre de notes" FROM public.sentiment WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "Sentiment";
    """
    df_pie_chart_sentiment = pd.read_sql_query(sql_pie_chart_sentiment, engine)
    pie_chart_sentiment_par_magasin = px.pie(
        data_frame=df_pie_chart_sentiment,
        names="Sentiment",
        values="Nombre de notes",
        category_orders={"Sentiment": ["Négatif", "Neutre", "Positif"]},
        color="Sentiment",
        color_discrete_map={
            "Négatif": "#EF553B",
            "Positif": "#00CC96",
            "Neutre": "#636EFA"})
    pie_chart_sentiment_par_magasin.update_layout(
        font={"size": 15},
        margin=dict(l=15, r=15, t=30, b=15),
        # legend=dict(
        #     yanchor="top",
        #     y=0.99,
        #     xanchor="left",
        #     x=0.005)
    )
    return pie_chart_sentiment_par_magasin

def get_word_cloud(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_wordcloud = f"""
        SELECT "processed_content_fr" FROM public.wordcloud WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}';
    """
    df_wordcloud = pd.read_sql_query(sql_wordcloud, engine)
    casto_mask = np.array(Image.open(file_setting.get("CASTO_LOGO_2")))
    casto_mask=np.where(casto_mask == 0, 255, casto_mask)
    text = " ".join(str(review) for review in df_wordcloud["processed_content_fr"])
    wc = WordCloud(background_color="white", max_words=100, mask=casto_mask, contour_color='firebrick')
    word_cloud = plt.figure()
    # Generate a wordcloud
    wc.generate(text)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    return word_cloud

def get_bar_chart_good_topics_par_magasin(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_bar_chart_good_topics = f"""
        SELECT "Topic" AS "Sujet", SUM("Count") AS "Nombre d'avis" FROM public.nmf_good WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "Topic" ORDER BY "Topic" DESC;
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

def get_bar_chart_bad_topics_par_magasin(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> Figure:
    sql_bar_chart_bad_topics = f"""
        SELECT "Topic" AS "Sujet", SUM("Count") AS "Nombre d'avis" FROM public.nmf_bad WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Month" >= '{selected_min_date}' AND "Month" <= '{selected_max_date}' GROUP BY "Topic" ORDER BY "Topic" DESC;
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

def get_table_raw_comments(engine: engine.base.Engine, selected_city: str, selected_address: str, selected_min_date: date, selected_max_date: date) -> None:
    sql_table_raw_comments = f"""
        SELECT "Date", "Rating" AS "Note", "Sentiment", "Content" AS "Avis" FROM public.raw_comments WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Date" >= '{selected_min_date}' AND "Date" < '{selected_max_date}' ORDER BY "Date";
    """
    df_table_raw_comments = pd.read_sql_query(sql_table_raw_comments, engine)
    gb = GridOptionsBuilder.from_dataframe(df_table_raw_comments)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    gridOptions = gb.build()
    AgGrid(df_table_raw_comments, gridOptions=gridOptions, height=500, width='100%', theme="fresh")