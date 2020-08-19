# jsd_job_bot
Shows which jobs are in my JSD queue

You need a `config.py` file:

    JSD_API_KEY = 'supersecretAPIkey'
    JSD_HOSTNAME = 'example.atlassian.net'
    JSD_USERNAME = 'user@example.com'
    SHOW_ALL_JOBS = False

Run it, it'll show you what you've got assigned to you.

Uses `pipenv` for dependencies, or you can run `pip install jira loguru python-dateutil click texttable`.


