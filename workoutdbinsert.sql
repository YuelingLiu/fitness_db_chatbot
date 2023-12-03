-- Script name: inserts.sql
-- Author:      Yueling Liu
-- Purpose:     insert sample data to test the integrity of this database system

-- the database used to insert the data into.
USE workoutdb;


 -- 1. workout class level table inserts
INSERT INTO level
    (level_id, level_name, `desc`)
VALUES 
    (1, 'Beginner', 'Suitable for those new to the exercise.'),
    (2, 'Intermediate', 'For those with some experience.'),
    (3, 'Advanced', 'For seasoned exercise enthusiasts.');


 -- 2. workout class type table inserts
INSERT INTO  type
    (type_id, type_name, `desc`)
VALUES 
	(110, 'Cardio', 'High-intensity cardiovascular workouts.'),
    (111, 'Strength Training', 'Exercises focused on building muscle strength.'),
    (112, 'Yoga Flex', 'Combines physical postures, meditation, and breathing exercises.');

-- 3. class schedule table inserts
INSERT INTO schedule
    (schedule_id, duration, start_time, end_time)
VALUES 
    (1550,   60, '2023-11-05 08:00:00', '2023-11-05 09:00:00'),   
    (1551,   30, '2023-11-06 10:00:00', '2023-11-06 10:30:00'),   
    (1552,   45, '2023-12-11 13:00:00', '2023-12-11 13:45:00'),
	(1553,   45, '2023-12-18 14:15:00', '2023-12-18 15:00:00'),
	(1554,   45, '2023-12-22 15:15:00', '2023-12-22 16:00:00'),
    (1555,   30, '2023-12-27 15:15:00', '2023-12-27 15:45:00');
      


 -- 4. account  table inserts
INSERT INTO  account
    (account_id, email, password, role, date_registered)
VALUES 
	
	(12343, 'admin0@example.com', 'securePass456', 'Admin', '2023-02-15'),
    (12344, 'admin1@example.com', 'securePass456', 'Admin', '2023-02-15'),
	(12345, 'TommyT@example.com', 'password123', 'Instructor', '2023-01-10'),
    (12346, 'Stella@example.com', 'securePass456', 'Admin', '2023-02-15'),
    (12347, 'bob@example.com', 'myPassword789', 'Instructor', '2023-03-20'),
  	(12348, 'zach@example.com', 'password123', 'Instructor', '2023-01-10' ),
    (12300, 'manager1@example.com', 'password123', 'Manager', '2023-01-10' ),
    (12301, 'manager2@example.com', 'securePass456', 'Manager', '2023-02-15'),
    (12302, 'manager3@example.com', 'myPassword789', 'Manager', '2023-03-20'),
    (12200, 'Member1@example.com', 'password123', 'Membership', '2023-01-10' ),
    (12201, 'Member2@example.com', 'securePass456', 'Membership', '2023-02-15'),
    (12202, 'Member3@example.com', 'myPassword789', 'Membership', '2023-03-20'),  
    (12203, 'manager1@example.com', 'password123', 'Membership', '2023-01-10' ),
    (12204, 'Member4@example.com', 'securePass456', 'Membership', '2023-02-15'),
    (12205, 'Member5@example.com', 'myPassword789', 'Membership', '2023-03-20'),
    (12206, 'employee1@example.com', 'password123', 'Employee', '2023-01-10' ),
    (12207, 'employee2@example.com', 'securePass456', 'Employee', '2023-02-15'),
    (12208, 'employee3@example.com', 'myPassword789', 'Employee', '2023-03-20');

 -- 5 . instructor table inserts
INSERT INTO instructor
    (instructor_id, name, email, phone, account_id, dob, ssn)
VALUES 
    (5100, 'Tommy T', 'TommyT@example.com', '234-567-8901',12345,'1988-02-12', '777-77-7777'),
    (5101, 'Bob B', 'BobBrown@example.com', '345-678-9012',12347,'1980-06-25', '888-88-8888'),
    (5102, 'Zach L', 'ZachL@example.com', '345-678-9012',12348,'1980-06-25', '888-88-8888');




-- 6. workout_class table inserts
INSERT INTO workout_class
    (class_id, level, class_title, location, type, instructor_id, schedule_id)
VALUES 
    (9900, 1, 'Cardio Blast', 'Room A',  110, 5100, 1550),
    (9901, 1, 'Strength Training', 'Room B', 111, 5101, 1551),
    (9902, 1, 'Yoga Flex', 'Room C', 112, 5100, 1552),
	(9903, 2, 'Yoga Pulse', 'Room C', 112, 5102, 1553),
    (9904, 2, 'Pilates Powerhouse', 'Room C', 112, 5102, 1552),
	(9905, 1, 'Circuit Cyclone ', '2Room C', 112, 5100, 1554);
      
    

-- 7. general member table inserts
INSERT INTO member
    (tracking_id, class_id, date)
VALUES 
    (3001, 9900, '2023-01-10 10:30:00'),
    (3002, 9900, '2023-02-15 14:00:00'),
    (3003, 9902, '2023-03-20 17:15:00');


-- 8. membership table inserts 
INSERT INTO membership
    (member_id, membership_tye, pricing, start_date, end_date, auto_pay, account_id)
VALUES 
    (888801, 'Basic', 999, '2023-01-01 00:00:00', '2024-01-01 00:00:00', 0, 12200),
    (888802, 'Premium', 1299, '2023-05-01 00:00:00', '2024-05-01 00:00:00', 0, 12201),
    (888803, 'Gold', 1599, '2023-08-01 00:00:00', '2024-08-01 00:00:00', 0, 12202);



-- 9. booking_history table inserts 
INSERT INTO booking_history
    (booking_id, member_id, class_id, booking_date, cancellation_date, status)
VALUES 
    (2001, 888801, 9900, '2023-01-05 09:30:00', NULL, 'Booked'),
    (2002, 888802, 9900, '2023-01-10 11:00:00', NULL, 'Booked'),
    (2003, 888803, 9901, '2023-01-15 16:45:00', NULL, 'Booked'),
	(2004, 888803, 9900, '2023-10-15 16:45:00', NULL, 'Booked'),
	(2005, 888803, 9904, '2023-10-27 16:45:00', NULL, 'Booked'),
	(2006, 888803, 9904, '2023-11-01 16:45:00', NULL, 'Booked');
    


-- 10. instructor certification table inserts 
INSERT INTO  certification
    (certification_id, instructor_id, name, issuing_organization, expiration_date)
VALUES 
    (30, 5100, 'Cardio Teacher Training', 'Yoga Alliance', '2025-01-15 00:00:00'),
    (31, 5101, 'Strength Certified Personal Trainer', 'ACE Fitness', '2024-06-20 00:00:00'),
    (32, 5102, 'Pilates Instructor Certificate', 'Pilates Method Alliance', '2026-12-10 00:00:00');


-- 11.  facility table inserts
INSERT INTO facility
    (facility_id, facility_name, address, city, state, postal_code, operation_hours, occupancy)
VALUES 
    (40, 'Downtown Fitness Center', '123 Main St', 'Fremont', 'CA', '94539', '6 AM - 10 PM', 100),
    (41, 'Uptown Gym', '456 High Rd', 'Gotham', 'GT', '95678', '5 AM - 9 PM', 75),
    (42, 'West Side Wellness', '789 Sunset Blvd', 'Riverdale', 'RV', '91201', '7 AM - 11 PM', 100);


-- 12. workout equipment table inserts 
INSERT INTO equipment 
    (equipment_id, name, quantity, serial_number, purchase_date, price, `condition`, last_maintenance_date, facility_id)
VALUES 
    (760, 'Treadmill', 40, 'T12345', '2021-01-10 00:00:00', 2000.00, 'Good', '2023-01-05 00:00:00', 40),
    (761, 'Dumbbell Set', 300, 'D98765', '2020-06-15 00:00:00', 500.00, 'Fair', '2023-02-20 00:00:00', 40),
    (762, 'Stationary Bike', 150, 'B45678', '2021-08-20 00:00:00', 1500.00, 'Excellent', '2023-03-15 00:00:00', 42);
 
 
 
  
-- 13. purchase table inserts
INSERT INTO purchase
    (transation_id, member_id, price, date, payment_method)
VALUES 
    (7001, 888801, 999, '2023-01-10 15:30:00', 'Credit Card'),
    (7002, 888801, 999, '2023-02-20 16:45:00', 'Debit Card'),
    (7003, 888803, 1599, '2023-03-05 14:00:00', 'PayPal');




-- 14. admin table inserts
INSERT INTO admin
    (admin_id, account_id, name, title, email, phone,dob,ssn)
VALUES 

    (501, 12346, 'Stella', 'Head Admin', 'Stella@example.com', '456-789-0123', '1993-04-10', '444-44-4444'),
    (502, 12343, 'Admin1', 'Assistant Admin', 'sneveu@example.com', '567-890-1234', '1975-08-18', '555-55-5555'),
    (503, 12344, 'Admin2', 'Senior Admin', 'teabing@example.com', '678-901-2345', '1965-11-05', '666-66-6666');



 -- 15. manager table inserts
INSERT INTO manager
(manager_id, name, phone, account_id, dob, ssn)

VALUES 
    (2001, 'manager1', '567-890-1234',12300, '1988-02-10', '777-77-7112'),
    (2002, 'manager2',  '678-901-2345',  12301, '1988-02-11', '777-77-0777'),
    (2003, 'manager3',  '789-012-3456',  12302,  '1988-02-12', '771-77-7777');


-- 16. review table inserts
INSERT INTO review
    (review_id, member_id, class_id, rating, comment, review_date)
VALUES 
    (7001, 888801, 9900, 4.5, 'Great class! Really enjoyed the session.', '2023-09-15 10:15:00'),
    (7002, 888802, 9901, 3.0, 'Good workout but the instructor went too fast.', '2023-09-18 16:20:00'),
    (7003, 888803, 9900, 5.0, 'Perfect class for relaxation. Highly recommended!', '2023-09-20 18:30:00');


-- 17. trainingGoal table inserts
INSERT INTO trainingGoal
    (goal_id, member_id, goal_type, start_date, target_date, Status)
VALUES 
    (801, 888801, 'Weight Loss', '2023-01-01 09:00:00', '2023-06-01 09:00:00', 'In Progress'),
    (802, 888802, 'Muscle Gain', '2023-02-15 10:00:00', '2023-08-15 10:00:00', 'Not Started'),
    (803, 888803, 'Flexibility', '2023-03-01 11:00:00', '2023-09-01 11:00:00', 'Completed');


-- 18. member_metrics table inserts :  weight is in lbs and height is feet and inches 
INSERT INTO metrics
    (record_id, member_id, weight, height)
VALUES 
    (901, 888801, 165, 512),  
    (902, 888802, 110, 502),
    (903, 888803, 178, 610);



-- 19. employee table inserts with account_id
INSERT INTO employee
    (employee_id, name, phone, hire_date, account_id, dob, ssn)
VALUES
    (4567,'employee1', '123-456-7890', '2022-01-15', 12206, '1985-12-25', '111-11-1111'),
    (4568, 'employee2', '234-567-8901', '2021-06-10', 12207, '1990-05-20', '222-22-2222'),
    (4569, 'employee3', '345-678-9012', '2020-09-05', 12208, '1982-03-15', '333-33-3333');



