def generate_query_to_search_with_default(keywords, size=10):
    return {
        "yql": "select title from simplewiki where userQuery();",
        "ranking": "default",
        "query": "title:{}".format(keywords),
        "hits": size,
    }


def generate_query_to_collect_features(keywords, size=10):
    return {}


def generate_query_to_search_with_mlr(keywords, size=10):
    return {}
