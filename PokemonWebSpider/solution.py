import multiprocessing
import random
from bs4 import BeautifulSoup
import requests

class Pokemon:
    def __init__(self, id, name, url, img_url, types):
        self.id = id
        self.name = name
        self.url = url
        self.img_url = img_url
        self.types = types
        #self.evolutions = evolutions
    def __str__(self):
        return f'<Poke {self.name} #{self.id}, types: {self.types}>'
    def __repr__(self):
        return str(self)
    
SOURCE_BASE = "https://pokemondb.net"
SOURCE = SOURCE_BASE + "/pokedex/national"
SOURCE_EV = SOURCE_BASE + "/evolution"

def get_pokemon_from_node(div):
    pokedex_url = div.a['href']
    img =  div.find("span", {"class": "img-sprite"})['data-src']
    id = int(div.small.text.strip('#'))
    name = div.find('a', {'class': 'ent-name'}).text
    types = list(map(lambda x: x.text, div.findAll('a', {'class': 'itype'})))
    pk = Pokemon(id, name, pokedex_url, img, types)
    return pk

def is_compatible_ev(id, evolutions, picked_id):
    for ev in evolutions:
        if id in ev: # found evolution where the current pick is possible
            for o_id in ev: # for all the possible participants of the family
                if o_id in picked_id: # if the evolution is already picked
                    return False
    return True

def pick_poke(picked_id, picked_types, pokemons, evolutions):
    while True:
        pick = random.choice(pokemons)
        if pick.id in picked_id or \
            len(pick.types) != 2 or \
            any(map(lambda x: ((pick.types[0] in x) and (pick.types[1] in x)),
                picked_types)) or \
            not is_compatible_ev(pick.id, evolutions, picked_id):
            continue
        return pick
    
def generate_team(pokemons, evolutions):
    PICK_N = 6
    picked_id = []
    picked_types = []
    for _ in range(PICK_N):
        picked = pick_poke(picked_id, picked_types, pokemons, evolutions)
        picked_id.append(picked.id)
        picked_types.append(picked.types)
    return list(filter(lambda x: x.id in picked_id, pokemons))


def get_pokemons():
    src_html = requests.get(SOURCE).content
    soup = BeautifulSoup(src_html, features="html.parser")

    cards = soup.findAll("div", {"class": "infocard"})
    return list(map(get_pokemon_from_node, cards))

def get_evolutions():
    src_html_ev = requests.get(SOURCE_EV).content
    soup = BeautifulSoup(src_html_ev, features="html.parser")

    evolutions = []
    for ev in soup.findAll('div', {'class': 'infocard-list-evo'}):
        ev_nums = []
        for card in ev.findAll('span', {'class': 'infocard-lg-data'}):
            ev_nums.append(int(card.small.text.strip('#')))
        evolutions.append(ev_nums)
    return evolutions

pokemons = get_pokemons()
evolutions = get_evolutions()

print(generate_team(pokemons, evolutions))

#TODO: Output cool Html...