# SQL to Databox

Answer to the question: How to move data from SQL server to [Databox](http://databox.com) with help from [Databox Python SDK](https://github.com/databox/databox-python)?

![License](http://img.shields.io/:license-mit-blue.svg)

## MySQL → Databox streaming Example

1. Create new empty `databox_example` database with stocks table.

    mysql -u root -vv < sql/mysql_recreate_database.sql
    
2. Start [mysql_streamer.py](mysql_streamer.py) script that will "observe" stocks table for new records and stream them into Databox.

    ./mysql_streamer.py databox_example -u root -t <databox push_token>
    
3. Open new command-prompt and insert few historical stock quotes with [stocks_downloader.py](stocks_downloader.py).

    ./stocks_downloader.py YHOO -g m -x sql | mysql -u root -vv databox_example;
    
Simple output from [mysql_streamer.py](mysql_streamer.py)
    
    ...
    Nothing to do. Sleeping,...
    Streaming from 454
    Inserted new records from 454,...
    Nothing to do. Sleeping,...
    Streaming from 460
    Inserted new records from 460,...
    Nothing to do. Sleeping,...
    Nothing to do. Sleeping,...
    Nothing to do. Sleeping,...
    ...

## Development

```bash
mkvirtualenv databox-python-sql
pip install --upgrade -v -r requirements.txt
```

## Author
- [Oto Brglez](https://github.com/otobrglez)