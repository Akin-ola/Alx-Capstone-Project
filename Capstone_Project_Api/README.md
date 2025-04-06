This is a project that form a part of graduation prerequsite of my Alx BE web development programme.

I choose to design a Task Management API for my unit in the Nigerian Air Force
Over the years there has been lack of maintenance record for equipment used in carrying out
various armament operations in the unit.
These has led to breakdown in maintenance culture, and short of operational standard required
of the unit.
Therefore I choose to do this project as a prototype to what can eliminate this bad phenomenal.

The Task management API project will focus on implementing task management using Django and Django
REST framework.

The project has implement four (4) models which includes;

    Technician (also the customuser model)
    Equipment model
    Task model
    Maintenance model

**The technician model will be the Customuser (members of the organisation) with the Commanding officer as
the Admin-user and and all other members as just users.

**The equipment will be a register for all the equipments available in the organisation, only the admin-user will be able to create, update or delete an equipment other member will only be permitted to carry out safe
(read-only) methods

**Task will be a register for any maintenance task arising from the usage of the equipments, example of a work-order
where all technician will have access to check and pick any pending task to do, the task are listed by the admin-user with pending status, immidiately a technician registered the task in the maintenance record, the task is mark as completed so that another technician won't go ahead to perform the same task.

**Maintenance will be a table of record for all the maintenance activities, a register for all completed tasks.
will be usefull in tracking the unit activities and also gives detail information about the equipment service life. Allowing the technicians to focus solely on carrying out their primary assignment of maintaining the equipments. 

I will be using the rest_framework TokenAuthentication for the users authentication, and rest_framework IsAuthenticated for their permission. In addition I implement a custom-permission for the admin-user which allow them to perform some certain activities. (IsAdminAuthenticatedUser).
I aslo implement another custom permission to be user for maintenance related endpoints, which allow only the user attach to a record to perform certain operations. (IsOwnerOrReadOnly).

I configured MySQL database in the project in place of the django SQLite3.

I had a database bug, I must add this to this file, it has to do with my customUser implementation, I had to drop the database for another one. Not as simple as this, I persevered.

The following are my API endpoints with their methods.

METHODS                  ENDPOINTS              FUNCTIONS

'POST'                 'login/',              for User login
'POST'                 'logout/',             for User logout also invalidate/delete user token until another login
'POST'                 'register/',           for User registration 
'GET'/'POST'           'equipments/',         for listing and creation of equipment record 
'GET'/'PUT'            'equipment/<int:pk>/', for retrieving an equipment or updating an equipment record 
'GET'/'POST'           'tasks/',              for listing and creating task
'GET'/'PUT'/'DELETE'   'task/<int:pk>/',      for retrieving, updating and deleting of task
'GET'/'POST'           'maintenance/',        for listing and creating maintenance record
'GET'/'PUT'/'DELETE'   'maintenance/<int:pk>/',     for retrieving, updating and deleting of maintenance record
'GET'                  'technicians/',        for listing all the user(technicians)
'GET'/'PUT'/'DELETE'   'technician/<int:pk>/',     for retrieving, updating and deleting of record
