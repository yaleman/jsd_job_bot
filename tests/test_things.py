""" doesn't really test much """


import dateutil.parser
from texttable import Texttable # type: ignore
from loguru import logger

def test_dateutil() -> None:
    """ does it really, though? """
    result = dateutil.parser.parse("2022-02-05T10:30Z")
    logger.debug(result)
    assert result


def test_texttable() -> None:
    """ or does it? """

    table = Texttable()
    table.set_cols_dtype(['a', 'a', 'a', 'a'])
    table.set_max_width(0)
    table.set_deco(Texttable.BORDER + Texttable.VLINES + Texttable.HEADER)
    table.add_row(['Issue', 'Status', 'Updated', 'Summary'])
    table.add_row(['FOO-1235', 'Blocked', '2022-05-04', 'This is a bad summary'])

    logger.info(table.draw())

    assert table
    assert "FOO-1235" in table.draw()
