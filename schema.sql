drop table if exists events;
create table events (
  id integer primary key autoincrement,
  dayNum integer not null,
  monthNum integer not null,
  yearNum integer not null,
  eventStatus integer not null,
  eventClaim text not null,
  eventDesc text not null,
  eventConfirms text not null,
  eventDenies text not null
);

drop table if exists users;
create table users (
	username text not null,
	passHash text not null,
  email text,
  notificationSettings text not null
);