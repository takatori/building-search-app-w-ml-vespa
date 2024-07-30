import os

import pandas as pd
import streamlit as st
from vespa.application import Vespa

from vespa_query import (
    generate_query_to_search_with_default,
    generate_query_to_search_with_mlr,
)

# streamlit UIオプション設定
st.set_page_config(layout="wide")

vespa = Vespa("http://vespa:8080")


# 検索キーワード
keywords = st.text_input("検索キーワードを入力してください", value="")

# 検索キーワードが空ならば、処理を打ち切る
if not keywords:
    st.stop()


default_query = generate_query_to_search_with_default(keywords, size=20)
default_result = vespa.query(body=default_query).hits
mlr_query = generate_query_to_search_with_mlr(keywords, size=20)
mlr_result = vespa.query(body=mlr_query).hits


default_cl, mlr_col = st.columns(2)

with default_cl:
    st.header("default")
    st.table(
        pd.DataFrame(
            [
                {"title": hit["fields"]["title"], "score": hit["relevance"]}
                for hit in default_result
            ]
        )
    )
with mlr_col:
    st.header("mlr")
    st.table(
        pd.DataFrame(
            [
                {"title": hit["fields"]["title"], "score": hit["relevance"]}
                for hit in mlr_result
            ]
        )
    )
