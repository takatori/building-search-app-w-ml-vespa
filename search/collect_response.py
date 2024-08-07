#!/usr/bin/env python

import warnings

from argparse import ArgumentParser
from vespa.application import Vespa

from vespa_query import (
    generate_query_to_search_with_default,
    generate_query_to_collect_features,
    generate_query_to_search_with_mlr,
)


def parse_response(response):
    titles = [hit["fields"]["title"] for hit in response.hits]
    features = [hit["fields"].get("summaryfeatures", None) for hit in response.hits]
    r = response.json
    hits = r["root"]["fields"]["totalCount"]
    took = (
        r["timing"]["querytime"]
        + r["timing"]["summaryfetchtime"]
        + r["timing"]["searchtime"]
    )

    return titles, features, hits, took


parser = ArgumentParser()
parser.add_argument("target", choices=["baseline", "feature", "mlr"])
parser.add_argument("output_path")
parser.add_argument("keywords_path")
parser.add_argument("--window-size", type=int, default=100)
parser.add_argument("--extract-hits-and-took", action="store_true")
args = parser.parse_args()

args.output_group_path = args.output_path + ".group"

# ハンズオンなので、DeprecationWarningを無効にしてコンソールを見やすくする
warnings.filterwarnings("ignore", category=DeprecationWarning)

extra_query_params = {}
if args.target == "baseline":
    generate_query_func = generate_query_to_search_with_default
elif args.target == "feature":
    generate_query_func = generate_query_to_collect_features
elif args.target == "mlr":
    generate_query_func = generate_query_to_search_with_mlr
    extra_query_params["window_size"] = args.window_size
else:
    raise ValueError(f"Unknown target: {args.target}")

vespa = Vespa("http://vespa:8080")

with open(args.keywords_path) as f, open(args.output_path, "w") as of, open(
    args.output_group_path, "w"
) as gf, vespa.syncio() as session:
    for keywords in f:
        keywords = keywords.strip()
        body = generate_query_func(keywords, **extra_query_params)
        try:
            response = session.query(body=body)
            titles, features, hits, took = parse_response(response)
            labels = [int(title == keywords) for title in titles]
            # target == featureのとき、label種類が2つ以上あるリクエストのみを結果に出力する
            # すべての関連度が等しい場合、関連度の順序関係を学習するランキング学習が適用できないため
            if args.target == "feature" and len(set(labels)) < 2:
                continue
            # --extract-hits-and-tookが指定されているとき: hitsとtookを空白区切りで出力する
            if args.extract_hits_and_took:
                of.write(f"{hits} {took}\n")
            # それ以外: labelとfeature情報（レスポンスに存在する場合のみ）を空白区切りで出力する
            else:
                for label, feature in zip(labels, features):
                    tokens = []
                    tokens.append(str(label))
                    if feature is not None:
                        for i, (feature_name, feature_value) in enumerate(
                            feature.items()
                        ):
                            tokens.append(f"{i}:{feature_value}")
                    of.write(f"{' '.join(tokens)}\n")
            gf.write(f"{len(titles)}\n")
        except Exception:
            continue  # ハンズオンなので何かしらで例外が発生した場合は無視する
