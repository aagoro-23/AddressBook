/*Creation of database and administrate table for Administrate exercise*/
CREATE DATABASE administrate;
CREATE TABLE contacts(organisation VARCHAR(50), 
	name VARCHAR(50), 
	email VARCHAR(50), 
	phonenumber VARCHAR(50),
	id INT AUTO_INCREMENT PRIMARY KEY);