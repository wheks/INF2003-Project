Airlines Database Management System (DBMS) User Manual
1. Introduction
   
●	Overview of the DBMS
    ○	Our Air Passenger Arrival Data Management System addresses critical challenges in tourism management and economic planning by consolidating fragmented air passenger data into a unified, comprehensive     database. This innovative system enables real-time analysis of arrival patterns, integrating information on passengers, countries of origin, length of stay, and airlines. It provides tourism boards, aviation authorities, and destination managers with powerful tools for data-driven decision-making. The system's capabilities extend to enhanced resource allocation, targeted marketing campaigns, improved tourist     experiences, and the promotion of sustainable tourism practices.

●	Key Features of the DBMS
    ○	Create, Read, Update, Delete (CRUD) for passenger data
    ○	Advanced Features: Analyse Airline Popularity, Analyse Tourism Duration, Analyse Airline Trend

2. Installation and Setup
●	Installation Guide PyCharm Community Version 
    ○	Install Pycharm Community Version
    ○	https://www.jetbrains.com/pycharm/download/?section=windows
 
●	Run the install and select where you would like to save it. Click ‘Next’. 
●	 In the following page as well click ‘Next’. 
●	Select JetBrains as the place to install and then click ’Next’
●	Let the programme run then click ‘Finish’ Once its done.
 
•	Open the python file of the code in Pycharm Community Edition 
•	Click the button near the bottom left of the interface search for respective packages to install.
•	Download the following packages: MariaDB, pandas, pymysql, sqlalchemy and ttkbootstrap.


•	Installation Guide for MariaDB 
    o	Install MariaDB here: https://mariadb.com/
    o	Create a password and user in mariaDB
    o	Create a database using the Query in MariaDB 
       ![image](https://github.com/user-attachments/assets/2087108a-6e2b-4e71-9332-76e376df903c)
    o	Exit mariaDB and open up command prompt.Download and ingest the sql file by opening command prompt outside of MariaDB 
    	Select the correct path in the command prompt of where the sqlfile is stored then add this line of code to ingest 
    ![image](https://github.com/user-attachments/assets/136f2bc5-e1a3-41b5-97be-caea6ecc6a19)
    	Log into MariaDB again and check if the database is updated.
    o	Update the following code in PyCharm to reflect your respective Username, Password and Database Name

![image](https://github.com/user-attachments/assets/0d78241c-3476-40bd-b440-65740624f3ef)

![image](https://github.com/user-attachments/assets/681546b3-08d4-4c8b-89fe-30e243c1df76)

       
•	Make sure to change username to the username you created! Password as well!
   Once done, open MariaDB and check with the database if it is now loaded and the code in python is updated to connect to MariaDB correctly, run the code.


3. Getting Started with the DBMS
•	Once the code is running, you will be greeted with a GUI
 
5. Performing Basic Operations
●	Create New Data: Select 'Create New Passenger" and fill in the respective Details
●	Read Data: Select 'Read Passenger Details' select by which parameter to search from an click search
●	Updating Data: Select 'Update Passenger' to Update passenger details
●	Deleting Data: Select 'Delete Passenger' to delete passenger details from table

6. Advanced Operations
●	Analyse Airline Popularity: Select 'Analyse Airline Popularity' to view most popular airline and the chart passenger count for each airlines
●	Analyse Tourism Duration: Select 'Analyse Tourism Duration' to view most common stayed duration and chart to compare each duration range
●	Analyse Airline Trend: Select 'Analyse Airline Trend' to view which airlines is the highest passenger from the respective country of origin


