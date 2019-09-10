/* START DROPS */

DROP TABLE IF EXISTS
  ClueWrongs
, ClueRights
, GameContestants
, Contestants
, Clues
, Categories
, Rounds
, Games;

/* END DROPS */

/* START CREATES */

CREATE TABLE Games (
  Id TEXT PRIMARY KEY NOT NULL, /* J-Archive Game ID */
  AirDate TEXT NOT NULL,
  Season TEXT NOT NULL,
  ShowNumber TEXT NOT NULL,
  BeforeDouble BOOLEAN NOT NULL,
  ContainedTiebreaker BOOLEAN NOT NULL DEFAULT FALSE,
  NoWinner BOOLEAN NOT NULL DEFAULT FALSE,
  UnknownWinner BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Rounds (
  Id SERIAL PRIMARY KEY NOT NULL,
  Name TEXT NOT NULL
); /* Jeopardy!, Double Jeopardy!, Final Jeopardy! */

CREATE TABLE Categories (
  Id TEXT PRIMARY KEY NOT NULL,
  GameId TEXT NOT NULL REFERENCES Games (id),
  RoundId INTEGER NOT NULL REFERENCES Rounds (id),
  Name TEXT
);

CREATE TABLE Clues (
  Id TEXT PRIMARY KEY NOT NULL,
  CategoryId TEXT NOT NULL REFERENCES Categories (id),
  Clue TEXT NOT NULL,
  Value INTEGER,
  Answer TEXT NOT NULL,
  DailyDouble BOOLEAN NOT NULL DEFAULT FALSE,
  DailyDoubleWager INTEGER,
  TripleStumper BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Contestants (
  Id TEXT PRIMARY KEY NOT NULL, /* J-Archive Contestant ID */
  FirstName TEXT,
  LastName TEXT,
  Profession TEXT,
  HomeTown TEXT,
  Gender TEXT, /* Retrieved through Genderize.io */
  GenderProbability DECIMAL, /* Retrieved through Genderize.io */
  Latitude TEXT, /* Retrieved through Google Maps Geocoding */
  Longitude TEXT /* Retrieved through Google Maps Geocoding */
);

CREATE TABLE GameContestants (
  GameId TEXT NOT NULL REFERENCES Games (id),
  ContestantId TEXT NOT NULL REFERENCES Contestants (id),
  Position INTEGER,
  Winner BOOLEAN NOT NULL DEFAULT FALSE,
  JeopardyTotal INTEGER,
  DoubleJeopardyTotal INTEGER,
  FinalJeopardyTotal INTEGER,
  FinalJeopardyWager INTEGER
);

CREATE TABLE ClueRights ( /* Answered clue correctly */
  ClueId TEXT NOT NULL REFERENCES Clues (id),
  ContestantId TEXT NOT NULL REFERENCES Contestants (id)
);

CREATE TABLE ClueWrongs ( /* Answered clue incorrectly */
  ClueId TEXT NOT NULL REFERENCES Clues (id),
  ContestantId TEXT NOT NULL REFERENCES Contestants (id)
);

/* END CREATES */

/* START CREATES */

INSERT INTO Rounds (Name) VALUES
 ('Jeopardy!')
,('Double Jeopardy!')
,('Final Jeopardy!');

/* END CREATES */
