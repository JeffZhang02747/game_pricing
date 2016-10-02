#img url example :
#https://store.playstation.com/store/api/chihiro/00_09_000/container/CA/en/999/UP9000-CUSA00900_00-SPEXPANSIONDLC03/1474345129000/image?_version=00_09_000&platform=chihiro&w=248&h=248&bg_color=000000&opacity=100

#search url example :
#https://store.playstation.com/chihiro-api/bucket-search/US/en/999/bloodborne?size=30&geoCountry=CA


#https://store.playstation.com/chihiro-api/search/CA/en/999/god%2Bof%2Bwar?bucket=games&game_content_type=games&size=30&geoCountry=CA
import requests
import urllib


search_url = "https://store.playstation.com/chihiro-api/search/CA/en/999/%s?bucket=games&game_content_type=games&size=30&geoCountry=CA"


best_api_key = "fjsr6ancrf4knq8vnxnyw82u"
best_search_endpointer = "https://api.bestbuy.com/v1/products(%s&(categoryPath.id=pcmcat295700050012))?apiKey=fjsr6ancrf4knq8vnxnyw82u&sort=regularPrice.asc&show=regularPrice,name&callback=JSON_CALLBACK&format=json"

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
		item["ps_price"] = None
		item["plus_price"] = None
		item["bestbuy_price"] = None

		insert_store_price(item, link)
		# insert_best_buy_price(item, link)

		res.append(item)
	return res


'''
helper func
insert best buy price to here
'''
def insert_best_buy_price(item, link):
	name = link["name"]
	name = name.encode('ascii', 'ignore')
	list_name = name.split(" ")
	
	for index in xrange(0, len(list_name)):
		inp = list_name[index]
		oup = ''.join(e for e in inp if e.isalnum())
		list_name[index] = oup

	query = '('
	last_index = len(list_name) - 1
	for index in xrange(0, last_index):
		name = list_name[index]
		query += "search=" + name
		query += "&"

	if last_index >= 0:
		query += "search=" + name
	query += ")"
	best_search = best_search_endpointer % (query)

	print best_search
	req = requests.get(best_search)
	response = req.json()

	print response

	if "products" not in response:
		return

	products = response["products"]
	for product in products:
		if "regularPrice" in product:
			item["bestbuy_price"] = product["regularPrice"]
			return
			

'''
helper func
given item and link,
insert ps price info to item
'''
def insert_store_price(item, link):
	if "default_sku" not in link:
		return

	sku = link["default_sku"]
	item["ps_price"] = sku["display_price"]

	if "rewards" not in sku:
		return

	rewards = sku["rewards"]
	for reward in rewards:
		if "is_plus" in reward and reward["is_plus"]:
			item["plus_price"] = reward["display_price"]
			return



# '''
# input: id of the game on PS store
# output: compare price to other vendors

# now just do this match by name, different vendors have different SKU for same game
# '''
# def price_compare(id):

# 	print id

