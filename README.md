# Jeopardy Archive Data

Scrape [J! Archive](http://j-archive.com/) for am extensive archive of Jeopardy!.

## Collecting the Data

1. Install [Python 3.7](https://www.python.org/downloads/) and the [Psycopg2](https://www.psycopg.org/docs/), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/), and [lxml](https://lxml.de/installation.html) packages.

2. Set up a **credentials.json** file in /credentials directory with PostgreSQL database information. Below is an example of a local database.

   ```json
   {
     "host": "localhost",
     "database": "jeopardy",
     "user": "postgres",
     "password": "password"
   }
   ```

3. To scrape the entire archive of the site, run the following command. This will create a collection in your database with all questions leading up to the most recent episode. It will take some time (between one and two hours).

   ```
   cd scrape
   python scrape.py -a
   ```

4. You can also scrape only specific seasons by running the command below. The example shown is for seasons 1 through 10 (will include 10).

   ```
   cd scrape
   python scrape.py -s 1 10
   ```

5. Set up a **keys.json** file in the /credentials directory with keys for [Genderize.io](https://genderize.io/) and the [Google Maps API](https://developers.google.com/maps/documentation)

   ```json
   {
     "gmaps_api_key": "key_here",
     "genderize_api_key": "key_here"
   }
   ```

6. Run the commands below to send the first name for each contestant to [Genderize.io](https://genderize.io/), a third-party API for identifying gender by name, and update the database accordingly.

   ```
   cd addon
   python gender.py
   ```

7. Run the commands below to update the database with the latitude and longitude for each contestant with a valid location.

   ```
   cd addon
   python geocode.py
   ```

## Topic Modeling

This project uses the topic modeling software [MALLET](http://mallet.cs.umass.edu/topics.php) to build a topic model for clues.

1. Run the command below to create a separate text file for each clue in the database from the first specified season to the last.

   ```
   cd topics
   python create_clues_data.py -s 1 35
   ```

2. Move to the MALLET directory on your local machine and import these files (specifically, point to the directory they are kept in).

   ```
   bin\mallet import-dir --input {wherever the project lives}\jeopardy-scrape\topics\mallet_files\data\clues --output jeopardy_clues.mallet --keep-sequence --remove-stopwords
   ```

3. Train the model and create the output files.

   ```
   bin\mallet train-topics --input jeopardy_prof.mallet --num-topics 25 --optimize-interval 20 --output-state jeopardy_prof_topic-state.gz --output-topic-keys jeopardy_prof_keys.txt --output-doc-topics jeopardy_prof_composition.txt
   ```

4. Move **jeopardy_prof_keys.txt** and **jeopardy_prof_composition.txt** to **topics/mallet_files/output/clues**. These files contain the topic information and which topics each clue is part of. Run the two commands below to update the database with that data.

   ```
   cd topics
   python parse_clue_topic_keys.py
   python parse_clue_topic_composition.py
   ```
