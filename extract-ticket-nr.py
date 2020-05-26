#!/usr/bin/env python3
from subprocess import check_output, CalledProcessError
import shlex
import re
import sys


EXCLUDED_BRANCHES = ("master")
JIRA_TICKET = re.compile(r"^[a-zA-Z]+-[0-9]+")


def prepend_ticket_nr():
    ticket_nr = None
    try:
        branch_name = "git symbolic-ref --short HEAD"
        current_branch = sh(branch_name)
        if current_branch not in EXCLUDED_BRANCHES:
            ticket_nr = extract_jira_ticket_nr(current_branch)
    except CalledProcessError:
        pass
    finally:
        prepend_commit_message(ticket_nr)


def sh(command):
    output = check_output(shlex.split(command))
    return output.decode("utf-8").replace("\n", "")


def extract_jira_ticket_nr(branch_name):
    ticket = JIRA_TICKET.match(branch_name)
    if ticket:
        return ticket.group().upper()


def prepend_commit_message(ticket_nr):
    with open(commit_message_file(), "r+") as msg:
        current_content = msg.read()
        next_content = (f"{ticket_nr} {current_content}"
                        if ticket_nr else current_content)
        msg.seek(0, 0)
        msg.write(next_content)


def commit_message_file():
    try:
        return sys.argv[1]
    except IndexError:
        return "/dev/null"


if __name__ == "__main__":
    prepend_ticket_nr()
