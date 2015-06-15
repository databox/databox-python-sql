# SQL to Databox

How to move data from SQL to [Databox](http://databox.com) with help from [Databox Python SDK](https://github.com/databox/databox-python)?

## MySQL Example

Create new empty `databox_example` database with stocks table.

    mysql -u root -vv < sql/mysql_recreate_database.sql
    
Start [mysql_streamer.py](mysql_streamer.py) script that will "observe" stocks table and stream results into Databox.

    ./mysql_streamer.py 
    
Then open new command-prompt, download a few historical stock quotes with help of [stocks_downloader.py](stocks_downloader.py) and insert them into stocks table.

    ./stocks_downloader.py YHOO -g m -x sql | mysql -u root -vv databox_example;
    
Simple output from mysql_streamer.py
    
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
