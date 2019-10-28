CREATE DATABASE loterry;
\connect loterry
CREATE TABLE results (
   ticket_id VARCHAR(7) UNIQUE NOT NULL,
   win BOOLEAN,
   ammount_of_Win integer
);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('0000001', FALSE, 0);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('0000002', FALSE, 0);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('0000003', FALSE, 0);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('0000004', TRUE, 2);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('0000005', FALSE, 0);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('0000006', FALSE, 0);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('0000007', TRUE, 5);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('0000008', FALSE, 0);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('1234567', TRUE, 0);
INSERT INTO results (ticket_id, win, ammount_of_Win)
    VALUES ('1234568', TRUE, 10);