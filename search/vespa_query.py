def generate_query_to_search_with_default(keywords, size=10):
    return {
        "yql": "select title from simplewiki where userInput(@userinput)",
        "userinput": keywords,
        "ranking": "default",
        "hits": size,
        "presentation.timing": True,
    }


def generate_query_to_collect_features(keywords, size=10):
    return {
        "yql": "select title, summaryfeatures from simplewiki where userInput(@userinput)",
        "userinput": keywords,
        "ranking": {"profile": "base"},
        "hits": size,
        "presentation.timing": True,
    }


def generate_query_to_search_with_mlr(keywords, size=10):
    return {}
