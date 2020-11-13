insert into patient(mail_id,P_name,age,blood_group,sex)
values
  ('a1@iiti.ac.in','john',22,'O+','M'),
  ('a2@iiti.ac.in','sudarsan',21,'B+','M'),
  ('a3@iiti.ac.in','pranavi',20,'O+','F'),
  ('a4@iiti.ac.in','shiva',18,'O+','M'),
  ('a5@iiti.ac.in','jagadesh',19,'AB+','M'),
  ('a6@iiti.ac.in','hritikesh',20,'B+','M'),
  ('a7@iiti.ac.in','sashi',20,'A+','M'),
  ('a8@iiti.ac.in','aniketh',21,'O+','M'),
  ('a9@iiti.ac.in','sharanya',19,'O+','F');


insert into medicines(medicine_id,medicine_name)
values
  (100000,'paracetmol'),
  (100001,'antihistamines'),
  (100003,'antacids'),
  (100004,'fabiflu'),
  (100005,'erythromycin'),
  (100006,'vitamin B'),
  (100007,'citrogen'),
  (100008,'calcium');

insert into takes(mail_id,medicine_id,quantity,takes_date)
values
  ('a1@iiti.ac.in',100000,5,'2019-07-11'),
  ('a1@iiti.ac.in',100004,3,'2019-07-11'),
  ('a1@iiti.ac.in',100005,7,'2019-07-19'),
  ('a3@iiti.ac.in',100007,5,'2019-09-11'),
  ('a4@iiti.ac.in',100001,6,'2019-11-11'),
  ('a4@iiti.ac.in',100003,1,'2019-11-11'),
  ('a2@iiti.ac.in',100008,20,'2020-06-11');

insert into specialization(spec_id,spec_name)
values
  (200000,'pediatrician'),
  (200001,'obstetrician'),
  (200002,'surgeon'),
  (200003,'psychiatrist'),
  (200004,'cardiologist'),
  (200005,'dermatologist'),
  (200006,'nephrologist'),
  (200007,'opthalmologist');

-- note in the doctor table we are storing the latest availaible date

insert into doctor(doctor_id,doctor_name,availaible_date)
values
  (300000,'pranavi','2020-11-12'),
  (300001,'steve','2020-09-12'),
  (300003,'pranavi','2020-11-14'),
  (300004,'rebecca','2020-10-12'),
  (300005,'adam','2020-11-08'),
  (300006,'fehlina','2020-10-12'),
  (300007,'ramaswamy ganeshan','2020-11-21'),
  (300008,'keerthi suresh','2020-12-12'),
  (300009,'john cena','2020-08-12');

-- created expert in table only if a new doctor is added
-- then there are null values associated if we dont know
-- specialization or u can consider it as a 4th NF
-- where doctor_id->>spec_name

insert into expert_in(doctor_id,spec_id)
values
  (300000,200000),
  (300000,200001),
  (300001,200000),
  (300005,200007),
  (300007,200006),
  (300007,200007),
  (300008,200004),
  (300008,200003);

insert into nurse(nurse_id,nurse_name,phone_number)
values
  (400000,'catalina',9247775899),
  (400001,'siri',9246665899),
  (400002,'loogle',9245555899),
  (400003,'cortana',9244445899),
  (400004,'sharanya',9241115899),
  (400005,'peter',9274775899),
  (400006,'nivin pauly',9249975899),
  (400007,'randomguy',9247775999);

insert into nursealloc(doctor_id,nurse_id,mail_id,date_in,date_out)
values
  (300000,400000,'a1@iiti.ac.in','2020-09-11','2020-09-13'),
  (300000,400000,'a2@iiti.ac.in','2020-08-14','2020-09-13'),
  (300000,400000,'a1@iiti.ac.in','2019-09-11','2019-09-13'),
  (300001,400003,'a5@iiti.ac.in','2020-07-14','2020-07-17'),
  (300003,400005,'a4@iiti.ac.in','2020-08-09','2020-08-14');

insert into appointment(mail_id,date_appointment,doctor_id)
values
  ('a1@iiti.ac.in','2020-11-08',300000),
  ('a1@iiti.ac.in','2020-11-08',300003),
  ('a1@iiti.ac.in','2020-08-11',300000),
  ('a2@iiti.ac.in','2020-09-14',300004),
  ('a3@iiti.ac.in','2020-09-22',300006),
  ('a4@iiti.ac.in','2020-09-23',300007),
  ('a5@iiti.ac.in','2020-11-08',300004);

insert into donation(donation_id,donation_type)
values
  (500000,'blood donation'),
  (500001,'plasma donation'),
  (500002,'kidney donation');

insert into donate(mail_id,donation_id,donation_date)
values
  ('a1@iiti.ac.in',500000,'2020-11-11'),
  ('a1@iiti.ac.in',500001,'2020-11-11'),
  ('a3@iiti.ac.in',500002,'2020-09-09'),
  ('a5@iiti.ac.in',500000,'2019-11-11');

insert into tests(test_id,test_name)
values
  (600000,'blood test'),
  (600001,'urine test'),
  (600002,'X ray'),
  (600003,'MRI scan'),
  (600004,'diabetic test'),
  (600005,'HIV test'),
  (600006,'covid19 test'),
  (600007,'wbc test');

insert into record(mail_id,record_id,record_analysis)
values
  ('a1@iiti.ac.in',100,'he got headache bla bla
    bla bla bla ....'),
  ('a1@iiti.ac.in',101,'he got stomachache bla bla
    bla bla bla ....'),
  ('a4@iiti.ac.in',100,'bla bla
    bla bla bla ....'),
  ('a6@iiti.ac.in',104,'bla bla
    bla bla bla ....'),
  ('a4@iiti.ac.in',102,'he got headache bla bla
      bla bla bla ....');

insert into test_descrp(mail_id,test_id,test_date,test_analysis)
values
  ('a2@iiti.ac.in',600000,'2020-09-11','bla bla bla ....
    bla bla bla .... bla bla bla ....'),
  ('a4@iiti.ac.in',600004,'2019-09-11','bla bla bla ....
    bla bla bla .... bla bla bla ....'),
  ('a2@iiti.ac.in',600002,'2020-08-11','bla bla bla ....
    bla bla bla .... bla bla bla ....'),
  ('a3@iiti.ac.in',600001,'2020-11-11','bla bla bla ....
    bla bla bla .... bla bla bla ....'),
  ('a5@iiti.ac.in',600006,'2020-08-15','bla bla bla ....
    bla bla bla .... bla bla bla ....');

insert into rooms(room_no,block_no)
values
  ('101a','bose'),
  ('101b','bose'),
  ('101a','kalam'),
  ('101b','kalam'),
  ('505','shivan'),
  ('303','steve');

insert into bookings(mail_id,room_no,block_no,date_in,date_out)
values
  ('a1@iiti.ac.in','101a','bose','2020-09-01','2020-09-08'),
  ('a3@iiti.ac.in','101a','kalam','2020-09-01','2020-09-08'),
  ('a1@iiti.ac.in','101a','bose','2019-09-01','2019-09-08'),
  ('a5@iiti.ac.in','505','shivan','2020-11-14','2020-11-15'),
  ('a4@iiti.ac.in','303','steve','2020-04-01','2020-05-01');
