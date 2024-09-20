ORDERS_PER_PAGE = 8


def get_page(items: list, page: int) -> list:
    start = page * ORDERS_PER_PAGE
    end = start + ORDERS_PER_PAGE
    return items[start:end]
