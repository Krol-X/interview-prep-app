---
title: "table, column, index, unique constraint, foreign key, migration, schema"
hot: false
sub: "4. База данных и тесты"
---
- **table / column / row** — *a column on the exchanges table.*
- **index** — *add an index on user_id*; **composite index** — составной; **partial index**.
- **unique constraint / unique index** — *a unique constraint on (event_id, recipient_id).*
- **foreign key** — *a foreign key to users.*
- **primary key**, **nullable / NOT NULL**, **default value**, **check constraint**.
- **migration** — *write / run / roll back a migration.*
- **schema** — *the schema is in schema.rb.*
- **to normalize / denormalize**.

> I'd enforce it at the database level — a unique index rather than a Rails validation, because the validation can't protect against two concurrent inserts.
