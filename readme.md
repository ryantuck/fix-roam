# fix-roam

A script to update UIDs for Roam Research graph exports.

## Usage

```
cat my-roam-export.json | python fixroam.py > updated-export.json
```

## Why?

Export your Roam graph, delete all your pages, and try to re-import that same graph. Roam will complain that `"blocks already exist"` and will fail to import, but won't give you more helpful info than that.

Updating UIDs appears to solve 99% of these issues.

### Note on debugging

It turns out that 4 / 474 of my notes still were inexplicably unable to import back into my graph, even after updating UIDs.

To find these, I basically outputted my script results and continuously whittled the result set down using `jq` like so:

```
$ cat my-roam-export.json | python fixroam.py  | jq 'length'
474
$ cat my-roam-export.json | python fixroam.py  | jq '.[0:256]' > subset.json
... attempt import, get error ...
$ cat my-roam-export.json | python fixroam.py  | jq '.[0:128]' > subset.json
... attempt import, get error ...
$ cat my-roam-export.json | python fixroam.py | jq '.[0:64]' > subset.json
... attempt import, no error!
$ cat my-roam-export.json | python fixroam.py  | jq '.[64:96]' > subset.json
... attempt import, get error ...

... and so on and so forth ...
```

After identifying the problematic notes, I added their titles to the `BLACKLIST` list in the script to remove them from the output, and kept on truckin' until I got the whole functioning batch to import.
