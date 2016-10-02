#img url example :
#https://store.playstation.com/store/api/chihiro/00_09_000/container/CA/en/999/UP9000-CUSA00900_00-SPEXPANSIONDLC03/1474345129000/image?_version=00_09_000&platform=chihiro&w=248&h=248&bg_color=000000&opacity=100

#search url example :
#https://store.playstation.com/chihiro-api/bucket-search/US/en/999/bloodborne?size=30&geoCountry=CA


#https://store.playstation.com/chihiro-api/search/CA/en/999/god%2Bof%2Bwar?bucket=games&game_content_type=games&size=30&geoCountry=CA
import requests
import urllib




search_url = "https://store.playstation.com/chihiro-api/search/CA/en/999/%s?bucket=games&game_content_type=games&size=30&geoCountry=CA"
'''
search games on ps store
'''
def search_games_ps_store(query):
	#first urllib encode the query so it can fit into the url
	query = urllib.quote(query)
	to_search_url = search_url % (query)

	#simple get request
	req = requests.get(to_search_url)
	response = req.json()

	if "links" not in response:
		return []

	links = response["links"]

	res = []

	for link in links:
		item = {}
		item["name"] = link["name"]
		item["id"] = link["id"]
		item["platform"] = link["playable_platform"]

		sku = link["default_sku"]

		item["price"] = sku["display_price"]
		item["plus_price"] = None

		rewards = sku["rewards"]
		for reward in rewards:
			if "is_plus" in reward and reward["is_plus"]:
				item["plus_price"] = reward["display_price"]

		res.append(item)
	return res
	
