CREATE TABLE IF NOT EXISTS users (
    id                  MEDIUMINT   NOT NULL,
    uuid                CHAR(36)    NOT NULL,
    displayName         TEXT,
    username            TEXT,
    age                 SMALLINT,
    bio                 MEDIUMTEXT,
    relationshipStatus  TINYTEXT,
    sexualOrientation   TINYTEXT,
    canHost             BOOLEAN,
    safeSex             TINYTEXT,
    PRIMARY KEY         (id)
);

CREATE TABLE IF NOT EXISTS sexualBehavior (
    uuid                CHAR(36)    NOT NULL,
    behavior            CHAR(36)    NOT NULL,
    PRIMARY KEY         (uuid, behavior)
);

CREATE TABLE IF NOT EXISTS social (
    uuid                CHAR(36)    NOT NULL,
    socialNetwork       CHAR(36)    NOT NULL,
    displayName         CHAR(36),
    value               CHAR(36),
    PRIMARY KEY         (uuid, socialNetwork)
);

CREATE TABLE IF NOT EXISTS locations (
    uuid                CHAR(36)    NOT NULL,
    place_id            INT         NOT NULL,
    place               CHAR(36)    NOT NULL,
    region              CHAR(36)    NOT NULL,
    country             CHAR(36)    NOT NULL,
    countryCode         CHAR(2)     NOT NULL,
    lon                 FLOAT       NOT NULL,
    lat                 FLOAT       NOT NULL,
    PRIMARY KEY         (uuid, place_id)
);

CREATE TABLE IF NOT EXISTS homeplaces (
    uuid                CHAR(36)    NOT NULL,
    place_id            INT         NOT NULL,
    place               CHAR(36)    NOT NULL,
    region              CHAR(36)    NOT NULL,
    country             CHAR(36)    NOT NULL,
    countryCode         CHAR(2)     NOT NULL,
    lon                 FLOAT       NOT NULL,
    lat                 FLOAT       NOT NULL,
    PRIMARY KEY         (uuid, place_id)
);

CREATE TABLE IF NOT EXISTS sonas (
    uuid                CHAR(36)    NOT NULL,
    sona_id             INT         NOT NULL,
    displayName         CHAR(36)    NOT NULL,
    description         MEDIUMTEXT,
    hasFursuit          BOOLEAN,
    speciesId           INT,
    speciesDisplayName  CHAR(36),
    PRIMARY KEY         (uuid, sona_id)
);

CREATE TABLE IF NOT EXISTS kinks (
    uuid                CHAR(36)    NOT NULL,
    kink_id             INT         NOT NULL,
    displayName         CHAR(36)    NOT NULL,
    categoryName        CHAR(36)    NOT NULL,
    receive             TINYINT,
    give                TINYINT,
    PRIMARY KEY         (uuid, kink_id)
);

CREATE TABLE IF NOT EXISTS user_groups (
    uuid                CHAR(36)    NOT NULL,
    group_id            INT         NOT NULL,
    displayName         CHAR(36)    NOT NULL,
    contentRating       TINYTEXT,
    PRIMARY KEY         (uuid, group_id)
);

CREATE TABLE IF NOT EXISTS genders (
    uuid                CHAR(36)    NOT NULL,
    gender              TINYTEXT
);

CREATE TABLE IF NOT EXISTS languages (
    uuid                CHAR(36)    NOT NULL,
    language            TINYTEXT
);

CREATE TABLE IF NOT EXISTS hobbies (
    uuid                CHAR(36)    NOT NULL,
    hobby_id            INT         NOT NULL,
    interest            TINYTEXT
);