def paginate_response(page, page_size, query):

    offset = (page-1) * page_size
    return query.offset(offset).limit(page_size).all()
