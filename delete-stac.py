#!/usr/bin/env python3

# python script that tries to delete 
# the given id from the stac catalog

# dependencies
# pip3 install requests
import json
import requests

# stac url
stachost="http://localhost:5000"

# case study item to be deleted
id = 'f9e34b5a-4752-419c-9a53-33372447199c'


# parse all available collections
# and gather the available collection ids
# e.g. sentinel5p
data = requests.get(url=stachost+'/collections').json()
collections=data['collections']
col_ids = [col['id'] for col in collections]


assoc_id=None
assoc_col=None
# for all available cases
# try to find the item's id
# based on the item's Products id
for col_id in col_ids:

    # for each collection
    # gather all items
    collection = requests.get(url='http://localhost:5000/collections/'+col_id+'/items').json()

    for item in collection['features']:

        # if the given id is found in the assets -> safe-manifest url
        # then the item's id is consider the one that is associated with the given id
        if "Products('{}')".format(id) in item['assets']['safe-manifest']['href']:
            assoc_col=col_id
            assoc_id=item['id']
            break

if assoc_id:
    # authorization must have been set
    # e.g. netrc
    # in order to be able to delete items
    # from stac catalog

    # deletes item via the python's requests library implementation
    url = "{}/collections/{}/items/{}".format(stachost,assoc_col,assoc_id)
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {access-token}"
    }

    # uncomment to use python for deletion

    #response = requests.delete(url, headers=headers)
    #print(response.status_code)

    # you can delete it manually by running
    print("Run in terminal:\n\
    curl -X DELETE {} -H \'Accept: application/json\'\
    -H \'Authorization: Bearer {{access-token}}\'".format(url, assoc_col, assoc_id))

else:
    print('No association for the {} is found'.format(id))














