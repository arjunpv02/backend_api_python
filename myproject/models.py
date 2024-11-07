from threading import Lock

# In-memory data storage
students_data = {}
next_id = 1
data_lock = Lock()
