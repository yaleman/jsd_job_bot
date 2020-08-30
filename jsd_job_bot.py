#!/usr/bin/env python3

""" polls JSD to find tickets I'm assigned to """

import os
from configparser import ConfigParser

import dateutil.parser
from jira import JIRA
import jira.exceptions
from texttable import Texttable


if not os.environ.get('LOGURU_LEVEL'):
    os.environ['LOGURU_LEVEL'] = "INFO"
from loguru import logger #pylint: disable=wrong-import-position,wrong-import-order

config = ConfigParser()
for config_file in ['~/.config/jsd_job_bot.ini',
                    '~/etc/jsd_job_bot.ini',
                    './jsd_job_bot.ini',
                    ]:
    if os.path.exists(config_file):
        logger.debug(f"Loading config: {config_file}")
        config.read(config_file)

# don't show things by default
if not config.has_option('DEFAULT', 'SHOW_ALL_JOBS'):
    logger.debug("Setting show all jobs to false, currently unset")
    config.set('DEFAULT', 'SHOW_ALL_JOBS', 'false')

JSD_SEARCH = """assignee = currentuser() ORDER BY updated ASC"""

IGNORED_STATUS = [
    'Completed',
    'Done',
    'Canceled',
    'Resolved',
    'Closed',
]

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
try:
    logger.debug(f"JIRA Server: '{config.get('DEFAULT', 'JSD_HOSTNAME')}'")
    logger.debug(f"JIRA Username: '{config.get('DEFAULT', 'JSD_USERNAME')}'")
    logger.debug(f"JIRA API Key: '{config.get('DEFAULT', 'JSD_API_KEY')}'")
    logger.debug("Instantiating JIRA connection...")
    jira_client_object = JIRA(
        f"https://{config.get('DEFAULT', 'JSD_HOSTNAME')}",
        basic_auth=(config.get('DEFAULT', 'JSD_USERNAME'), config.get('DEFAULT', 'JSD_API_KEY')),
        )
    logger.debug("Done instantiating JIRA connection...")
except ConnectionError as error_message:
    logger.error(f"Connection error: {error_message}")

try:
    logger.debug("Searching for jobs assigned to you...")
    issues = jira_client_object.search_issues(jql_str=JSD_SEARCH, maxResults=False)
    # noqa: pylint: disable=invalid-name
except jira.exceptions.JIRAError as error_message:
    logger.error(error_message)
    exit()

for issue in issues:
    logger.debug(f"issue status: '{issue.fields.status}'")
    if config.getboolean('DEFAULT', 'SHOW_ALL_JOBS') or str(issue.fields.status).strip() not in IGNORED_STATUS:
        ASSIGNED_ISSUES += 1
        updated_parsed = dateutil.parser.parse(issue.fields.updated)

        logger.debug(f"{issue}\t{issue.fields.status}\t{updated_parsed.date()}\t{issue.fields.summary}")
        table.add_row([str(issue),
                       str(issue.fields.status),
                       updated_parsed.date(),
                       str(issue.fields.summary),
                       ])
        #logger.debug([dirfield for dirfield in dir(issue.fields) if not ignore_this_field(dirfield)])
print(table.draw())

logger.info(f"{ASSIGNED_ISSUES} tickets assigned to you...")
