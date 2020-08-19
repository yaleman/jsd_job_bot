#!/usr/bin/env python3

""" polls JSD to find tickets I'm assigned to """

import os
import dateutil.parser

from jira import JIRA
from texttable import Texttable
from config import JSD_API_KEY, JSD_HOSTNAME, JSD_USERNAME, SHOW_ALL_JOBS

if not os.environ.get('LOGURU_LEVEL'):
    os.environ['LOGURU_LEVEL'] = "INFO"
from loguru import logger #pylint: disable=wrong-import-position,wrong-import-order

jira_client_object = JIRA(
    f"https://{JSD_HOSTNAME}",
    basic_auth=(JSD_USERNAME, JSD_API_KEY),
    )

JSD_SEARCH = """assignee = currentuser() ORDER BY updated ASC"""

IGNORED_STATUS = [
    'Completed',
    'Done',
    'Canceled',
    'Resolved'
]


issues = jira_client_object.search_issues(jql_str=JSD_SEARCH, maxResults=False) # noqa: pylint: disable=invalid-name

def ignore_this_field(fieldname):
    """ filters fields """
    if fieldname.startswith("_"):
        return True
    elif fieldname.startswith("customfield"):
        return True
    return False

ASSIGNED_ISSUES = 0
table = Texttable()
table.set_cols_dtype(['a', 'a', 'a', 'a'])
table.set_max_width(0)

table.set_deco(Texttable.BORDER + Texttable.VLINES + Texttable.HEADER)

table.add_row(['Issue', 'Status', 'Updated', 'Summary'])



for issue in issues:
    if SHOW_ALL_JOBS or str(issue.fields.status) not in IGNORED_STATUS:
        ASSIGNED_ISSUES += 1
        updated_parsed = dateutil.parser.parse(issue.fields.updated)

        logger.debug(f"{issue}\t{issue.fields.status}\t{updated_parsed.date()}\t{issue.fields.summary}")
        table.add_row([str(issue),
                       str(issue.fields.status),
                       updated_parsed.date(),
                       str(issue.fields.summary),
                       ])
        logger.debug([dirfield for dirfield in dir(issue.fields) if not ignore_this_field(dirfield)])
print(table.draw())

logger.info(f"{ASSIGNED_ISSUES} tickets assigned to you...")
