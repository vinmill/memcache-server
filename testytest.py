import pickle
filename_directory = 'memcache.pickle'

with open(filename_directory, 'wb') as f:
    pickle.dump({key : value}, f)

new_dict_ = {i:i for i in range(10)}

with open(filename_directory, 'rb') as f:
    new_dict_.update(pickle.load(f))

with open(filename_directory, 'wb') as f:
    pickle.dump( new_dict_ , f)

# Open the file in binary mode
with open(filename_directory, 'rb') as f:
      
    # Call load method to deserialze
    myvar = pickle.load(f)
  
    print(myvar)