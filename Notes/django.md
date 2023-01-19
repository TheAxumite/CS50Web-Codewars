# Utilizing Django Model Methods

objects.all()\ - Retrieves all the records from the database for a particular model. 
objects.filter(=)\ - Retrieves a queryset of records from the database that match the specified field/value pair. 
objects.exclude(=)\ - Retrieves a queryset of records from the database that do not match the specified field/value pair. 
objects.get(=)\ - Retrieves a single record from the database that matches the specified field/value pair. 
save()\ - Saves a record to the database. 
delete()\ - Deletes a record from the database. 
objects.create(=, ...)\ - Creates a new record in the database and saves it. 
objects.update(=, ...)\ - Updates one or more fields on all records that match a queryset filter, and saves them to the database 
objects.values()\ - Retrieves specified fields from the database, return them in a dictionary format 
objects.values_list()\ - Retrieves specified fields from the database, return them in a tuple format

# Utilizing Django Model Fields

field.default\ - the default value of the field
field.primary_key\ - whether the field is a primary key
field.unique\ - whether the field must be unique
field.null\ - whether the field can be null
field.blank\ - whether the field can be blank
field.choices\ - the choices available for the field
field.help_text\ - the help text for the field
field.verbose_name\ - the verbose name for the field
field.editable\ - whether the field is editable
field.db_column\ - the name of the column in the database
