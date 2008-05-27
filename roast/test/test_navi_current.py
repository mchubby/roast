from nose.tools import (
    eq_ as eq,
    assert_raises,
    )

from roast import navi_current

def test_empty():
    g = navi_current.navi_mark_current(
        navigation=iter([]),
        current='/foo',
        )
    assert_raises(StopIteration, g.next)

def test_simple():
    def g():
        yield dict(
            link='/something-else',
            title='something else',
            )
    g = navi_current.navi_mark_current(
        navigation=g(),
        current='/foo',
        )
    got = g.next()
    eq(
        got,
        dict(
            link='/something-else',
            title='something else',
            current=False,
            ),
        )
    assert_raises(StopIteration, g.next)

def test_current():
    def g():
        yield dict(
            link='/foo',
            title='foo',
            )
    g = navi_current.navi_mark_current(
        navigation=g(),
        current='/foo',
        )
    got = g.next()
    eq(
        got,
        dict(
            link='/foo',
            title='foo',
            current=True,
            ),
        )
    assert_raises(StopIteration, g.next)
