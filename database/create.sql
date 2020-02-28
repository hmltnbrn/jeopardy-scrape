/* START DROPS */

DROP TABLE IF EXISTS
  clue_wrongs
, clue_rights
, game_contestants
, contestants
, profession_topics
, clues
, clue_topics
, categories
, rounds
, games;

/* END DROPS */

/* START CREATES */

CREATE TABLE games (
  id TEXT PRIMARY KEY NOT NULL, /* J-Archive Game ID */
  air_date TEXT NOT NULL,
  season TEXT NOT NULL,
  show_number TEXT NOT NULL,
  before_double BOOLEAN NOT NULL,
  contained_tiebreaker BOOLEAN NOT NULL DEFAULT FALSE,
  all_star_game BOOLEAN NOT NULL DEFAULT FALSE,
  no_winner BOOLEAN NOT NULL DEFAULT FALSE,
  unknown_winner BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE rounds (
  id SERIAL PRIMARY KEY NOT NULL,
  round_name TEXT NOT NULL
); /* Jeopardy!, Double Jeopardy!, Final Jeopardy! */

CREATE TABLE categories (
  id TEXT PRIMARY KEY NOT NULL,
  game_id TEXT NOT NULL REFERENCES games (id),
  round_id INTEGER NOT NULL REFERENCES rounds (id),
  category_name TEXT
);

CREATE TABLE clue_topics (
  id INTEGER PRIMARY KEY NOT NULL,
  run_weight DECIMAL NOT NULL,
  full_text TEXT NOT NULL,
  short_text TEXT
);

CREATE TABLE clues (
  id TEXT PRIMARY KEY NOT NULL,
  category_id TEXT NOT NULL REFERENCES categories (id),
  clue_text TEXT NOT NULL,
  clue_value INTEGER,
  answer TEXT NOT NULL,
  daily_double BOOLEAN NOT NULL DEFAULT FALSE,
  daily_double_wager INTEGER,
  triple_stumper BOOLEAN NOT NULL DEFAULT FALSE,
  topic_id INTEGER REFERENCES clue_topics (id),
  topic_weight DECIMAL,
  topics_all JSONB
);

CREATE TABLE profession_topics (
  id INTEGER PRIMARY KEY NOT NULL,
  run_weight DECIMAL NOT NULL,
  full_text TEXT NOT NULL,
  short_text TEXT
);

CREATE TABLE contestants (
  id TEXT PRIMARY KEY NOT NULL, /* J-Archive Contestant ID */
  first_name TEXT,
  last_name TEXT,
  profession TEXT,
  hometown TEXT,
  gender TEXT, /* Retrieved through Genderize.io */
  gender_probability DECIMAL, /* Retrieved through Genderize.io */
  latitude TEXT, /* Retrieved through Google Maps Geocoding */
  longitude TEXT, /* Retrieved through Google Maps Geocoding */
  profession_topic_id INTEGER REFERENCES profession_topics (id),
  profession_topic_weight DECIMAL,
  profession_topics_all JSONB
);

CREATE TABLE game_contestants (
  game_id TEXT NOT NULL REFERENCES games (id),
  contestant_id TEXT NOT NULL REFERENCES contestants (id),
  position INTEGER,
  winner BOOLEAN NOT NULL DEFAULT FALSE,
  jeopardy_total INTEGER,
  double_jeopardy_total INTEGER,
  final_jeopardy_total INTEGER,
  final_jeopardy_wager INTEGER,
  UNIQUE (game_id, contestant_id)
);

CREATE TABLE clue_rights ( /* Answered clue correctly */
  clue_id TEXT NOT NULL REFERENCES clues (id),
  contestant_id TEXT NOT NULL REFERENCES contestants (id),
  UNIQUE (clue_id, contestant_id)
);

CREATE TABLE clue_wrongs ( /* Answered clue incorrectly */
  clue_id TEXT NOT NULL REFERENCES clues (id),
  contestant_id TEXT NOT NULL REFERENCES contestants (id),
  UNIQUE (clue_id, contestant_id)
);

/* END CREATES */

/* START CREATES */

INSERT INTO rounds (round_name) VALUES
 ('Jeopardy!')
,('Double Jeopardy!')
,('Final Jeopardy!');

/* END CREATES */
