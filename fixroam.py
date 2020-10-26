"""
Update all Roam UIDs to enable re-importing exported notes.

Usage:

    cat my-roam-export.json | python fixroam.py > updated-export.json
"""
import fileinput
import json
import random
import string

UID_MAP = dict()

# NOTE: Roam might just not want to import a note! When you identify these, blacklist them and rerun.
BLACKLIST = []


def read_stdin():
    return "".join(line for line in fileinput.input())


def generate_uid():
    """
    Generates a 9-digit UID that adheres to Roam's UID namespace.
    """
    namespace = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_"
    return "".join(random.choice(namespace) for _ in range(9))


def find_uids(data):
    """
    Recursively find all UIDs for blocks and update UID_MAP to map them to new values.
    """
    if isinstance(data, list):
        return [find_uids(x) for x in data]
    if isinstance(data, dict):
        if "uid" in data:
            existing_uid = data["uid"]
            if existing_uid in UID_MAP:
                new_uid = UID_MAP[existing_uid]
            else:
                new_uid = generate_uid()
                UID_MAP[existing_uid] = new_uid
        return {k: find_uids(v) for k, v in data.items()}
    return data


def main():
    """
    Read Roam JSON export from stdin and output a valid Roam JSON file with updated UIDs.
    """

    # read in graph
    data = read_stdin()
    graph = json.loads(data)

    # traverse the entire graph and populate UID_MAP, mapping old to new UIDs
    _ = find_uids(graph)
    assert set(UID_MAP.keys()) & set(UID_MAP.values()) == set()

    # filter to notes that Roam will actually accept
    valid_notes = [note for note in graph if not note["title"] in BLACKLIST]

    # create JSON string blob, swap out old UIDs with new values, and print to stdout
    # NOTE: it'd be nice if this were more efficient
    body = json.dumps(valid_notes, indent=2, ensure_ascii=False)
    for existing_uid, new_uid in UID_MAP.items():
        body = body.replace(existing_uid, new_uid)
    print(body)


if __name__ == "__main__":
    main()
