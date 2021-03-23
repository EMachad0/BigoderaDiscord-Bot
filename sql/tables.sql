-- drop table users

create table users (
	discord_user varchar(200),
	handle varchar(200),
	primary key (discord_user)
);

INSERT INTO users (discord_user, handle) VALUES
('Gasparini#9143', 'viniciuszeiko'),
('igorzera#5345', 'iorg'),
('João Vitor#1147', 'jvf'),
('Weiss#1983', '_Weiss'),
('jnk#9477', 'jnk');