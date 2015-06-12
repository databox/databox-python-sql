# SQL to Databox

How to move data from SQL to [Databox](http://databox.com) with help from [Databox Python SDK](https://github.com/databox/databox-python)?

## MySQL Example

Create new empty `databox_example` database with stocks table.

    mysql -u root -vv < sql/mysql_recreate_database.sql
    
Get a few historical stock quotes and load them into `stocks` table.

    ./stocks_downloader.py YHOO -g m -x sql | mysql -u root -vv databox_example;

## Development

```bash
mkvirtualenv databox-python-sql
pip install --upgrade -r requirements.txt
```
