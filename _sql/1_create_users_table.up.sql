CREATE TABLE users (
    twitter_user_id   TEXT       not null PRIMARY KEY,
    wallet_address    TEXT       not null,           --アドレス
    cultivation_coins REAL       not null,           --栽培中のもやし
    total_rain        REAL       not null DEFAULT 0, --累計rain
    created_at        TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
);