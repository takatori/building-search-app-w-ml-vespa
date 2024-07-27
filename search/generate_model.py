#!/usr/bin/env python

import json

from xgboost import DMatrix, train


feature_names = [
    "queryTermCount",
    "nativeRank",
    "attribute(pageviews)",
    "vespa.summaryFeatures.cached",
]


# XGBoost学習パラメータ
params = {
    "objective": "rank:pairwise",  # LambdaMARTによるランク学習
    "eval_metric": "ndcg",  # nDCGの評価値を学習ログに出力
    "tree_method": "hist",
    "grow_policy": "lossguide",
    "max_leaves": 60,
    "subsample": 0.45,
    "eta": 0.1,
    "seed": 0,
}

# 訓練データセット
training_input = DMatrix(
    "tmp/hands_on_featuredata.txt.training?format=libsvm", feature_names=feature_names
)

# 検証データセット
validation_input = DMatrix(
    "tmp/hands_on_featuredata.txt.validation?format=libsvm", feature_names=feature_names
)

# モデルの学習
evals = [(training_input, "train"), (validation_input, "valid")]
bst = train(
    params,
    training_input,
    num_boost_round=200,
    evals=evals,
    early_stopping_rounds=50,
    verbose_eval=10,
)

# モデルの出力
bst.dump_model(
    "tmp/hands_on_model.json",
    # fmap="tmp/feature-map.txt",
    with_stats=False,
    dump_format="json",
)
