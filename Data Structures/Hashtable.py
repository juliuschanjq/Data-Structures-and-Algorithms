# Create a dictionary
dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}

# Remove an entry with key 'Name'
del dict['Name']

# Clear all entries in the dictionary
dict.clear()

# Delete the entire dictionary
del dict

# Attempting to access the dictionary after deletion will result in an error.
# You can't access 'dict' after it's been deleted.

# The following lines would raise a KeyError because the dictionary no longer exists:
# print "dict['Age']: ", dict['Age']
# print "dict['School']: ", dict['School']
