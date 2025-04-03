This is a project that form a part of graduation prerequsite of my Alx BE web development programme.
I choose to design a Task Management API for my unit in the Nigerian Air Force
Over the year there has been lack of maintenance record of equipment used in carrying out
various armament operations in the unit.
These has led to breakdown in maintenance culture, and short of operational standard required
of the unit.

Therefore I choose to do this project as a prototype to what can eliminate this bad phenomenal
The Task management project will focus on implementing task management API using Django and Django
REST framework.

I have so far implement the models for my project which includes;

Technician class (also the custom user model)
Equipment class
Task class
Maintenance class

The technician will be the users (members of the organisation)
The equipment will be a table for all the equipments available in the organisation
Task will be a table for any maintenance task arising from the usage of the equipments
Maintenance will be a table of record for all the maintenance activities that has been done.

I will be using the rest_framework Token authentication for the users authentications
and rest_framework IsAuthenticated for their permission.

