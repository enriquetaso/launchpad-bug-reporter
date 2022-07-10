#! /usr/bin/python3

from datetime import datetime, timedelta, timezone

from launchpadlib.launchpad.Launchpad import login_anonymously

LP_PROJECTS = ["cinder", "os-brick", "cinderlib", "cinder-tempest-plugin"]
LP_PROJECT = "cinder"
LP_ENV = "production"  # or 'staging'
LP_LINK = "https://bugs.launchpad.net/%s/+bug/%d"

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

# The documents you retrieve from Launchpad will be stored here, which
# will save you a lot of time.
cachedir = "~/launchpad-bug-reporter/.launchpadlib/cache/"


def main():
    days_to_subtract = 10
    utc_end_date = datetime.now(tz=timezone.utc)
    utc_start_date = utc_end_date - timedelta(days=days_to_subtract)

    # Anonymous and read-only access to public Launchpad data
    lp = login_anonymously("testing", "production", cachedir, version="devel")

    basic_mgs = f"""Bug Report from {utc_start_date:%Y-%m-%d}
    to {utc_end_date:%Y-%m-%d} with IMPORTANCE={IMPORTANCE[0]}"""
    print(basic_mgs)

    for lp_project in LP_PROJECTS:
        print(f"\n{lp_project}\n---")
        project = lp.projects[lp_project]

        tasks = project.searchTasks(
            created_since=utc_start_date,
            created_before=utc_end_date,
            importance=IMPORTANCE[0],
        )

        if len(tasks) == 0:
            msg = f"""No bugs from {utc_start_date:%Y-%m-%d}
            to {utc_end_date:%Y-%m-%d}"""
            print(msg)
        else:
            for task in tasks:
                bug = task.bug
                link = LP_LINK % (lp_project, bug.id)
                info = f"""Bug #{bug.id} - {bug.title}\n
                Date {bug.date_created:%Y-%m-%d}\nLink {link}\n"""
                print(info)


if __name__ == "__main__":
    main()
