import requests
import shutil
import wget

image_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/"
filename = "1.png"

r = requests.get(image_url, stream = True)

for i in range(1,387):
	
	filename = str(i) + ".png"
	print(filename)
	image_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/" + str(filename)
	
	
	
	image_filename = wget.download(image_url)

