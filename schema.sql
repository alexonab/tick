CREATE TABLE "public"."quotes"
(
    "time"   int8,
    "symbol" varchar(8),
    "open"   float8,
    "high"   float8,
    "low"    float8,
    "close"  float8,
    "volume" int8
);

CREATE INDEX ON quotes (symbol, time);