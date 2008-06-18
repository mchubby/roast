from nose.tools import (
    eq_ as eq,
    assert_raises,
    )

from roast import explicit_navi

class Navigation_Test(object):

    def test_one(self):
        g = explicit_navi.get_navigation("""\
==========
Navigation
==========

Title1
======
First text
""")

        got = g.next()
        eq(
            got,
            dict(
                link='/title1',
                title='Title1',
                description='First text',
                ),
            )
        assert_raises(StopIteration, g.next)

    def test_two(self):
        g = explicit_navi.get_navigation("""\
==========
Navigation
==========

Title1
======
First text

Title2
======
More text
""")

        got = g.next()
        eq(
            got,
            dict(
                link='/title1',
                title='Title1',
                description='First text',
                ),
            )

        got = g.next()
        eq(
            got,
            dict(
                link='/title2',
                title='Title2',
                description='More text',
                ),
            )

        assert_raises(StopIteration, g.next)

    def test_one_child(self):
        from nose.exc import SkipTest
        raise SkipTest("""TODO no hierarchy yet""")
        g = explicit_navi.get_navigation("""\
==========
Navigation
==========

Title1
======
First text

Subtitle1
---------
More text
""")

        got = g.next()
        eq(
            got,
            dict(
                link='/title1',
                title='Title1',
                description='First text',
                children=[
                    dict(
                        link='/title1/subtitle1',
                        title='Subtitle1',
                        description='More text',
                        ),
                    ],
                ),
            )
        assert_raises(StopIteration, g.next)

    def test_link(self):
        g = explicit_navi.get_navigation("""\
==========
Navigation
==========

Title1
======
:link: foo

First text
""")

        got = g.next()
        eq(
            got,
            dict(
                link='/foo',
                title='Title1',
                description='First text',
                ),
            )
        assert_raises(StopIteration, g.next)

    def test_link_multiple(self):
        g = explicit_navi.get_navigation("""\
==========
Navigation
==========

Title1
======
:link: foo

First text

Title2
======
:link: bar

Second text
""")

        got = g.next()
        eq(
            got,
            dict(
                link='/foo',
                title='Title1',
                description='First text',
                ),
            )
        got = g.next()
        eq(
            got,
            dict(
                link='/bar',
                title='Title2',
                description='Second text',
                ),
            )
        assert_raises(StopIteration, g.next)
