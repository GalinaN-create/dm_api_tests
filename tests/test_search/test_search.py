def test_search(grpc_search):
    response = grpc_search.search(
        query='test_post',
        skip=0,
        size=10,
        search_across=['FORUM_TOPIC']
    )
