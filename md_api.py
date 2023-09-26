# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import xml.etree.ElementTree as ET
import urllib.request

# ids = {'1210': '1210', 'abalone': 'abalone', 'achi': 'achi', 'asalto': None, 'atarigo': 'ago', 'ataxx': None,
# 				 'baghchal': 'baghchal', 'blocking': None, 'cambio': None, 'change': None, 'chungtoi': 'ctoi',
# 				 'connections': None, 'criticalmass': None, 'dao': 'dao', 'dinododgem': 'dinododgem', 'dodgem': None,
# 				 'dotsandboxes': 'dnb', 'dragonsandswans': 'swans', 'fandango': None, 'fourfieldkono': None,
# 				 'foxandgeese': 'foxes', 'go': None, 'gobblet': None, 'hasamishogi': None, 'hex': None,
# 				 'horseshoe': None, 'iceblocks': None, 'joust': None, 'lewthwaitesgame': None, 'lgame': 'Lgame',
# 				 'linesofaction': None, 'lite3': None, 'mancala': 'mancala', 'mutorere': None, 'nim': None,
# 				 'ninemensmorris': '369mm', 'nutictactoe': None, 'oddoreven': 'ooe', 'othello': 'othello',
# 				 'paradux': None, 'pentago': None, 'pylos': None, 'quarto': None, 'queensland': None,
# 				 'quickchess': 'quickchess', 'quickcross': None, 'rubikscheckers': None, 'rubiksmagic': None,
# 				 'rubixinfinity': None, 'seega': None, 'shifttactoe': None, 'sim': 'sim', 'sliden': None,
# 				 'snake': 'snake', 'squaredance': None, 'tactix': None, 'threespot': '3spot', 'tictacchec': None,
# 				 'tictactier': None, 'tictactoe': 'ttt', 'tilechess': 'tilechess', 'tootandotto': None, 'topitop': None,
# 				 'winkers': None, 'wuzhi': None, 'xigua': None, 'connect4': 'connect4'}


def read_from_link(url):
	try:
		r = urllib.request.urlopen(url, timeout=2).read()
	except urllib.error.URLError:
		return None
	d = convert_xml_dict(r)
	return dict_to_markdown(d)


def parse_list_items(bag, child, name):
	if child.tag == name:
		bag[name] = []
		for r in child:
			bag[name].append(r.text)
		return True
	return False


def parse_nested(bag, child, name, key_tag='name', value_tag='description'):
	if child.tag == name:
		bag[name] = []
		for sub_child in child:
			key = ''
			value = ''
			for sub_sub_child in sub_child:
				if sub_sub_child.tag == key_tag:
					key = sub_sub_child.text
				elif sub_sub_child.tag == value_tag:
					value = sub_sub_child.text
			bag[name].append({key: value})
		return True
	return False


def convert_xml_dict(xml_string):
	root = ET.fromstring(xml_string)
	d = {}
	for child in root:
		processed = parse_nested(d, child, "strategies")
		if processed:
			continue
		processed = parse_nested(d, child, "variants")
		if processed:
			continue
		processed = parse_nested(d, child, "links", key_tag="url", value_tag="description")
		if processed:
			continue
		processed = parse_list_items(d, child, "references")
		if processed:
			continue
		processed = parse_list_items(d, child, "gamescrafters")
		if processed:
			continue
		d[child.tag] = child.text
	# print(child.tag, child.text)
	return d


def dict_to_markdown(d):
	text = ''
	text += f'## History\n{d["history"]}\n\n'
	text += f'## The Board\n{d["board"]}\n\n'
	text += f'## The Pieces\n{d["pieces"]}\n\n'
	text += f'## Rules\n{d["tomove"]}\n{d["towin"]}\n\n'

	text += f'## Strategies\n'
	for d1 in d["strategies"]:
		for k, v in d1.items():
			text += f'{k}: {v}\n'
	text += '\n'

	text += f'## Variants\n'
	for d1 in d["variants"]:
		for k, v in d1.items():
			text += f'{k}: {v}\n'
	text += '\n'

	text += f'## Links\n\n'
	for d1 in d["links"]:
		for k, v in d1.items():
			text += f'[{v}]({k})\n'
	text += '\n'

	text += f'## References\n\n'
	for r in d['references']:
		text += f' - {r}\n'
	text += '\n'

	text += f'## Gamescrafters\n\n'
	for g in d['gamescrafters']:
		text += f' - {g}\n'

	return text


def read_from_file(file):
	with open(file, 'r') as reader:
		content = reader.read()
		d = convert_xml_dict(content)
		print(dict_to_markdown(d))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	read_from_link('http://gamescrafters.berkeley.edu/games/1210.xml')
	print('---------------------------------------------------------\n')
	read_from_link('http://gamescrafters.berkeley.edu/games/baghchal.xml')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
