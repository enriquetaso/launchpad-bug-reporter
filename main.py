#! /usr/bin/python3

from datetime import datetime, timezone, timedelta
from launchpadlib.launchpad import Launchpad

LP_PROJECTS = ['cinder', 'os-brick', 'cinderlib', 'cinder-tempest-plugin']
LP_PROJECT = 'cinder'
LP_ENV = 'production'  # or 'staging'
LP_LINK = 'https://bugs.launchpad.net/%s/+bug/%d'

# These filter the types of bugs we want (i.e. anything open)
STATUSES = [
    'New',
    'Incomplete',
    'Confirmed',
    'Triaged',
    'In Progress',
    'Fix Committed',
]

IMPORTANCE = [
    'Undecided',
    'Low',
    'Medium',
    'High',
    'Critical',
    'Wishlist',
]

# The documents you retrieve from Launchpad will be stored here, which
# will save you a lot of time.
cachedir = "~/launchpad-bug-reporter/.launchpadlib/cache/"

days_to_subtract = 10
utc_end_date = datetime.now(tz=timezone.utc)
utc_start_date = utc_end_date - timedelta(days=days_to_subtract)

# Anonymous and read-only access to public Launchpad data
lp = Launchpad.login_anonymously(
    'testing',
    'production',
    cachedir,
    version='devel')

for lp_project in LP_PROJECTS:
    print(f"{lp_project}")
    print("---")
    project = lp.projects[lp_project]

    tasks = project.searchTasks(
        created_since=utc_start_date,
        created_before=utc_end_date,
        importance=IMPORTANCE[1])

    if len(tasks) == 0:
        print(f'No bugs from {utc_start_date:%Y-%m-%d} '
              f'to {utc_end_date:%Y-%m-%d}')
    for task in tasks:
        bug = task.bug
        link = LP_LINK % (lp_project, bug.id)
        print(f"- Bug #{bug.id}")
        print(f" Date {bug.date_created}")
        print(f" Link {link}")
