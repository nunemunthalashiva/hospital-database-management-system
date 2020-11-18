create table patient(
mail_id varchar(20) not null,
passwd varchar(20) not null,
P_name varchar(30) not null,
age numeric(2) not null,
blood_group varchar(3) not null,
sex char(1) not null,
primary key (mail_id)
);

create table doctor(
doctor_id varchar(6) not null,
passwd varchar(29) not null,
doctor_name varchar(30) not null,
availaible_date date ,
primary key (doctor_id)
);

create table appointment(
mail_id varchar(20) not null,
date_appointment date not null,
doctor_id varchar(6) not null,
primary key(mail_id,date_appointment,doctor_id),
foreign key (mail_id) references patient(mail_id),
foreign key(doctor_id) references doctor(doctor_id)
);

create table medicines(
medicine_id varchar(6) not null,
medicine_name varchar(30) not null,
primary key(medicine_id)
);

create table takes(
mail_id varchar(20) not null,
medicine_id varchar(6) not null,
quantity numeric(3) not null,
takes_date date not null,
primary key(mail_id,medicine_id,takes_date),
foreign key (medicine_id) references medicines(medicine_id),
foreign key (mail_id) references patient(mail_id)
);

create table specialization(
spec_id varchar(6) not null,
spec_name varchar(20) not null,
primary key(spec_id)
);

create table expert_in(
doctor_id varchar(6) not null,
spec_id varchar(6) not null,
primary key(doctor_id,spec_id),
foreign key(doctor_id )references doctor(doctor_id),
foreign key(spec_id) references specialization(spec_id)
);

create table nurse(
nurse_id varchar(6) not null,
nurse_name varchar(20) not null,
phone_number numeric(10) not null,
primary key (nurse_id)
);

create table nursealloc(
doctor_id varchar(20) not null,
nurse_id varchar(6) not null,
mail_id varchar(20) not null,
date_in date not null,
date_out date,
primary key(mail_id,date_in),
foreign key (mail_id) references patient(mail_id),
foreign key (nurse_id) references nurse(nurse_id),
foreign key(doctor_id )references doctor(doctor_id)
);

create table donation(
donation_id varchar(6) not null,
donation_type varchar(20) not null,
primary key(donation_id)
);

create table donate(
mail_id varchar(20) not null,
donation_id varchar(6) not null,
donation_date date not null,
primary key(mail_id,donation_date,donation_id),
foreign key (mail_id) references patient(mail_id),
foreign key (donation_id) references donation(donation_id)
);



create table tests(
test_id varchar(6) not null,
test_name varchar(20) not null,
primary key(test_id)
);

create table record(
mail_id varchar(20) not null,
record_id varchar(6) not null,
record_analysis text,
primary key(mail_id,record_id),
foreign key(mail_id) references patient(mail_id)
);

create table test_descrp(
mail_id varchar(20) not null,
test_id varchar(6) not null,
test_date date,
test_analysis text,
primary key(mail_id,test_id,test_date),
foreign key(test_id) references tests(test_id),
foreign key(mail_id) references patient(mail_id)
);

create table rooms(
room_no varchar(6),
block_no varchar(6),
primary key(room_no,block_no)
);

create table bookings(
mail_id varchar(20),
room_no varchar(6),
block_no varchar(6),
date_in date,
date_out date,
primary key(mail_id,date_in),
foreign key (mail_id) references patient(mail_id),
foreign key(room_no,block_no) references rooms(room_no,block_no)
);

create table receptionist(
mail_id varchar(20),
passwd varchar(20),
receptionist_name varchar(20)
);

insert into patient values('cse@ac.in','123','shiva',18,'o+','m');
insert into patient values('cse@ac.ip','1234','shiva',18,'o+','m');
insert into patient(mail_id,passwd,P_name,age,blood_group,sex)
values
  ('a1@iiti.ac.in','123','john',22,'O+','M'),
  ('a2@iiti.ac.in','123','sudarsan',21,'B+','M'),
  ('a3@iiti.ac.in','123','pranavi',20,'O+','F'),
  ('a4@iiti.ac.in','123','shiva',18,'O+','M'),
  ('a5@iiti.ac.in','123','jagadesh',19,'AB+','M'),
  ('a6@iiti.ac.in','123','hritikesh',20,'B+','M'),
  ('a7@iiti.ac.in','123','sashi',20,'A+','M'),
  ('a8@iiti.ac.in','123','aniketh',21,'O+','M'),
  ('a9@iiti.ac.in','123','sharanya',19,'O+','F');
  
insert into medicines(medicine_id,medicine_name)
values
  ('100000','paracetmol'),
  ('100001','antihistamines'),
  ('100003','antacids'),
  ('100004','fabiflu'),
  ('100005','erythromycin'),
  ('100006','vitamin B'),
  ('100007','citrogen'),
  ('100008','calcium');
  
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

  

insert into doctor(doctor_id,passwd,doctor_name,availaible_date) values
('300000','123','pranavi','2020-11-12'),
('300001','245','shiva','2020-11-12');

insert into doctor(doctor_id,passwd,doctor_name,availaible_date)
values
  ('300003','123','pranavi','2020-11-14'),
  (300004,'123','rebecca','2020-10-12'),
  (300005,'123','adam','2020-11-08'),
  (300006,'123','fehlina','2020-10-12'),
  (300007,'123','ramaswamy ganeshan','2020-11-21'),
  (300008,'123','keerthi suresh','2020-12-12'),
  (300009,'123','john cena','2020-08-12');

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

insert into appointment(mail_id,date_appointment,doctor_id)
	values
  ('cse@ac.in','2020-11-12','300000'),
  ('cse@ac.ip','2020-10-12','300001');
insert into donation(donation_id,donation_type)
values
  (500000,'blood donation'),
  (500001,'plasma donation'),
  (500002,'kidney donation');

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


insert into rooms(room_no,block_no) values ('101A','kalam'),('101B','raman');
insert into rooms(room_no,block_no)
values
  ('101a','bose'),
  ('101b','bose'),
  ('101b','kalam'),
  ('505','shivan'),
  ('303','steve');
