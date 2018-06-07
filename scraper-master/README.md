scraper
=======

[![Join the chat at https://gitter.im/openeventdata/scraper](https://badges.gitter.im/openeventdata/scraper.svg)](https://gitter.im/openeventdata/scraper?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Scrapes sites. Gets news. Eventually events.

More information can be found in the
[documentation](http://oeda-scraper.readthedocs.org/en/latest/).


###Installation

You should probably create a [virtual environment](http://www.virtualenv.org/en/latest/), but
in any event doing `pip install -r requirements.txt` should do the trick. You
might (probably will) have to specify something along the lines of 
`--allow-all-external pattern --allow-unverified pattern` for the pattern
library since it gets downloaded from its homepage. 

The scraper requires  a running MongoDB instance to dump the scraped stories into. 
Make sure you have MongoDB [installed](http://docs.mongodb.org/manual/installation/) 
and type `mongod` at the terminal to begin the instance if your install method
didn't set up the MongoDB process to run automatically. MongoDB doesn't require you to prepare
the collection or database ahead of time, so when you run the program it should automatically
create a database called `event_scrape` with a collection called `stories`. Once you've run  `python scraper.py`, 
you can verify that the stories are in the Mongo database by opening a new terminal window and typing `mongo`. 
 
To interface with Mongo, enter `mongo` at the command line. From inside Mongo, type `show dbs` to verify that there's a database called `event_scrape`. 
Enter the database with `use event_scrape` and type `show collections` to make sure there's a `stories` collection. 
 `db.stories.find()` will show you the first 20 entries.

###Running

After everything is installed, it's as simple as `python scraper.py`. That is
assuming, of course, that you wish to use the configuration seen in the
`default_config.ini` file. If not, just modify that. For the source type
section of the config, the three types of sources are `wire`, `international`,
and `local`. It is possible to specify any combination of those source types,
with the source types separated by commas in the config file. For more
information on the source types, see the **Contributing** section below.

###Contributing

More RSS feeds are always useful. If there's something specific you want to
see, just add it in and open a pull request with the source's raw XML RSS feed,
a unique source ID, a label indicating whether the source is
"international" or "local," and what language the site uses. We currently
support English and Arabic in the scraper.

We face a tradeoff between seeking the broadest geographic coverage we can get
(meaning including every local paper we can find) and accuracy and relevance
(which would lead us to include only large, well-known, and high quality news
outlets). We're trying to balance the two objectives by including a third
column indicating whether the source is one is a wire service, a dependable
news source with solid international coverage, or a local source that may
contribute extra noise to the data and may require specialized actor
dictionaries. The distinction between the latter two is hazy and requires a
judgement call. Eventually, these labels can be used to build event datasets
that are either optimized for accuracy and stability (at the cost of
sparseness), or micro-level, geographically dispersed (but noisy) coverage.
