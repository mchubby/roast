"""
Flag the current page (and parents) in navigation data.
"""

def navi_mark_current(navigation, current):
    for item in navigation:
        link = item.get('link')
        item['current'] = False
        if link is not None:
            if link == current:
                item['current'] = True
        yield item
