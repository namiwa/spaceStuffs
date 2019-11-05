import requests

# Would need to attain permission, else use the browser but data base is there

api_url = 'https://discosweb-api.sdo.esoc.esa.int/api/objects'
satnos = [
        8062, 9931, 10423, 10489, 10855, 10981, 11645, 12544,
        12546, 13010, 13011, 14095, 14128, 15386, 15875, 20122,
        20169, 21574, 22065, 23560, 23715, 23726, 25023, 25989,
        26410, 26411, 26463, 26464, 26958, 27386, 27540, 27816,
        27949, 28169, 28544, 28894, 28901, 28922, 32686, 32781,
        34602, 34937, 34938, 36036, 36037, 36508, 37368, 37846,
        37847, 38096, 38857, 38858, 39159, 39175, 39451, 39452,
        39453, 39479, 39634, 40103, 40697, 41043, 41335, 41388,
        41456, 42063, 42969, 43196, 43437
]

# get objects
objects = []
current_page = 0
while True:
    params = {'satno': satnos, 'page': current_page, 'sort': 'name'}
    result = requests.get(api_url, auth=('username', 'password'),
            params=params)
    if result.status_code == 200:
        result_dict = result.json()
        for object_ in result_dict['content']:
            objects.append(object_)
        if current_page < result_dict['totalPages']:
            current_page += 1
        else:
            break
    else:
        result.raise_for_status()

