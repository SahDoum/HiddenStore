ORDERS_PER_PAGE = 3


def get_page(items: list, page: int) -> list:
    start = page * ORDERS_PER_PAGE
    end = start + ORDERS_PER_PAGE
    return items[start:end]
