------------------------ PROFILE TABLE ------------------------          
CREATE TABLE Profile (
    user_id SERIAL PRIMARY KEY,
    name varchar,
    age int,
    location varchar(50),
    total_points int,
    total_co2e_reduced int
);
INSERT INTO profile(
        name,
        age,
        location,
        total_points,
        total_co2e_reduced
    )
VALUES ('bob', 11, 'Seattle, WA', 0, 0);
INSERT INTO profile(
        name,
        age,
        location,
        total_points,
        total_co2e_reduced
    )
VALUES ('mary', 15, 'New York City, NY', 0, 0);
INSERT INTO profile(
        name,
        age,
        location,
        total_points,
        total_co2e_reduced
    )
VALUES ('doris', 18, 'Las Vegas, NV', 0, 0);
CREATE TABLE plantbased_activity (
    id SERIAL PRIMARY KEY,
    user_id int,
    eco_breakfast bool,
    eco_lunch bool,
    eco_dinner bool,
    co2_reduced int,
    ecomeals_points int,
    CONSTRAINT user_id FOREIGN KEY(user_id) REFERENCES profile(user_id)
);
------------------ PLANTBASED ACTIVITY TABLE ------------------          
INSERT INTO plantbased_activity(
        user_id,
        eco_breakfast bool,
        eco_lunch bool,
        eco_dinner bool,
        co2_reduced int,
        ecomeals_points int,
    )
VALUES (
        3,
        false,
        true,
        false,
        15,
        20
    );
INSERT INTO plantbased_activity(
        user_id,
        eco_breakfast bool,
        eco_lunch bool,
        eco_dinner bool,
        co2_reduced int,
        ecomeals_points int,
    )
VALUES (
        2,
        true,
        false,
        false,
        15,
        20
    );
INSERT INTO plantbased_activity(
        user_id,
        eco_breakfast bool,
        eco_lunch bool,
        eco_dinner bool,
        co2_reduced int,
        ecomeals_points int,
    )
VALUES (
        3,
        false,
        false,
        true,
        15,
        20
    );
------------------ ECOTRANSPORT TABLE ------------------          
CREATE TABLE ecotransport (
    id SERIAL PRIMARY KEY,
    user_id int,
    activity varchar(50),
    co2_reduced int,
    ecoTransport_point int,
    activity_date date,
    distance int,
    CONSTRAINT user_id FOREIGN KEY(user_id) REFERENCES profile(user_id)
);
INSERT INTO ecotransport(
        user_id,
        activity,
        co2_reduced,
        ecoTransport_point,
        activity_date,
        distance
    )
VALUES (
        1,
        'walk',
        5,
        10,
        '2023-10-18',
        3
    );
INSERT INTO ecotransport(
        user_id,
        activity,
        co2_reduced,
        ecoTransport_point,
        activity_date,
        distance
    )
VALUES (
        2,
        'biking',
        20,
        40,
        '2023-10-18',
        5
    );
INSERT INTO ecotransport(
        user_id,
        activity,
        co2_reduced,
        ecoTransport_point,
        activity_date,
        distance
    )
VALUES (
        3,
        'car',
        0,
        0,
        '2023-10-18',
        10
    );
------------------ ECOEDUCATION TABLE ------------------          
CREATE TABLE ecoeducation (
    id SERIAL PRIMARY KEY,
    user_id int,
    activity_date date,
    points int,
    text text,
    CONSTRAINT user_id FOREIGN KEY(user_id) REFERENCES profile(user_id)
);
INSERT INTO ecoeducation(
        user_id,
        activity_date,
        points,
        text
    )
VALUES (
        1,
        '2023-10-18',
        20,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    );
INSERT INTO ecoeducation(
        user_id,
        activity_date,
        points,
        text
    )
VALUES (
        2,
        '2023-10-19',
        20,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    );
INSERT INTO ecoeducation(
        user_id,
        activity_date,
        points,
        text
    )
VALUES (
        3,
        '2023-10-20',
        20,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    );