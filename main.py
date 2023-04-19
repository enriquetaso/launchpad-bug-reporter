#! /usr/bin/python3
import os
from datetime import datetime, timedelta, timezone

from launchpadlib.launchpad import Launchpad as LP

from rich.console import Console
from rich.table import Table

from dotenv import load_dotenv

load_dotenv()

LP_PROJECTS = os.getenv("LP_PROJECTS", "cinder").split(",")
LP_PROJECT = os.getenv("LP_PROJECT", "cinder")
LP_ENV = os.getenv("LP_ENV", "production")  # or 'staging'
LP_LINK = os.getenv("LP_LINK", "https://bugs.launchpad.net/%s/+bug/%d")
LP_REASON = os.getenv("LP_REASON", "testing")
LP_VERSION = os.getenv("LP_VERSION", "devel")

# These filter the types of bugs we want (i.e. anything open)
STATUSES = [
    "New",
    "Incomplete",
    "Confirmed",
    "Triaged",
    "In Progress",
    "Fix Committed",
]

IMPORTANCE = [
    "Undecided",
    "Low",
    "Medium",
    "High",
    "Critical",
    "Wishlist",
]


def _create_table(project_name, start_date, end_date):
    table = Table(
        title=f"{project_name.capitalize()} Bugs from {start_date:%Y-%m-%d} to {end_date:%Y-%m-%d}"
    )
    table.add_column("Date", justify="right", style="cyan", no_wrap=True)
    table.add_column("Bug #", justify="right", style="magenta")
    table.add_column("Importance", style="magenta")
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="magenta")
    table.add_column("Assignee", style="magenta")
    table.add_column("Link", style="green")
    return table


def main():
    # The documents you retrieve from Launchpad will be stored here, which
    # will save you a lot of time.
    # get path to this directory
    path_dir = os.path.dirname(os.path.realpath(__file__))
    cachedir = os.getenv("LP_CACHE_DIR", f"{path_dir}/.launchpadlib/cache/")
    print(f"Using cache dir: {cachedir}")

    if not os.path.exists(cachedir):
        os.makedirs(cachedir)
    days_to_subtract = int(os.getenv("DAYS_TO_SUBTRACT", 7))
    utc_end_date = datetime.now(tz=timezone.utc)
    utc_start_date = utc_end_date - timedelta(days=days_to_subtract)

    # Anonymous and read-only access to public Launchpad data
    lp = LP.login_anonymously(LP_REASON, LP_ENV, cachedir, version=LP_VERSION)

    for lp_project in LP_PROJECTS:
        # Rich table
        table = _create_table(lp_project, utc_start_date, utc_end_date)

        # Launchpad
        project = lp.projects[lp_project]

        tasks = project.searchTasks(
            created_since=utc_start_date,
            created_before=utc_end_date,
            # importance=IMPORTANCE[0],
        )

        if len(tasks) == 0:
            table.add_row(
                "No bugs found",
                "",
                "",
                "",
                "",
                "",
                "",
            )

        else:
            for task in tasks:
                bug = task.bug
                link = LP_LINK % (lp_project, bug.id)

                assignee_status = "Unassigned"
                if task.assignee:
                    assignee_status = "Yes"

                bug_date = bug.date_created.strftime("%Y-%m-%d")
                bug_id = f"#{bug.id}"

                table.add_row(
                    bug_date,
                    bug_id,
                    task.importance,
                    bug.title,
                    task.status,
                    assignee_status,
                    link,
                )

        console = Console()
        console.print(table)


if __name__ == "__main__":
    main()
