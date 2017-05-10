import requests
import json
import os
stateImage = 'stateImage'

states_abbr = json.load(open('us_states_abbr.json.txt'))
print (states_abbr)
for key in states_abbr:

    abr = states_abbr[key]
    abrL= abr.lower()
    print (abrL)
    url = 'http://quarterdesigns.com/winners/{}_winner.jpg'.format(abrL)
    print(url)
    imageResponse = requests.get(url, stream = True)
    filename ='{}.jpg'.format(abr)
    filepath = os.path.join(stateImage, filename)
    with open(filepath, 'wb') as file:

        for chunk in imageResponse.iter_content(chunk_size=128):
            file.write(chunk)

# import requests
# import json
# import os
# stateImage = 'stateImage'
# imageURLs = []
# urlStateList = []
#
#
# states_abbr = json.load(open('us_states_abbr.json.txt'))
# state_list = list(states_abbr.keys())
# for state in state_list:
#     lowerState = state.lower()
#     urlState = lowerState.replace(' ','-')
#     urlStateList.append(urlState)
# testURLs = ['https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2000-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#     'https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/1999-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#     'https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2001-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#     'https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2002-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#     'https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2003-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#     'https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2004-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#     'https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2005-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#     'https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2006-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#     'https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2007-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#     'https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2008-50-state-quarters-coin-{}-proof-reverse-150x150.jpg',
#
#     ]
# print (urlStateList)
# for item in urlStateList:
#     for url in testURLs:
#         address =url.format(item)
#         response = requests.get(address)
#         #print (response.text)
#         ind = response.text.find('Forbidden')
#         if ind == -1:
#             #imageURLs.append([val, url])
#             imageURLs.append(address)
#             break
# print (imageURLs)
# print(len(imageURLs))
