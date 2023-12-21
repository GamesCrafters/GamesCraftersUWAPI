import xml.etree.ElementTree as ET
import urllib.request
import re

locale_map = {
	'en-US': 'eng',
	'es': 'spa'
}

def read_from_link(url):
	"""
	It is entirely possible that the requested url does not point
	to valid XML. Must have this try-except.
	"""
	try:
		r = urllib.request.urlopen(url, timeout=2).read()
		d = convert_xml_dict(r)
		instructions = dict_to_markdown(d)
		return instructions
	except:
		return ""

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
	return d

def renderString(s, code):
	replaced = re.sub(r"\[img\s+src\s*=\s*\"([^\"]*)\"([^\]]+)\]", rf"![alt](http://gamescrafters.berkeley.edu/instructions/i/{code}/\1)", s)
	return re.sub(r"\[br\]", "\n\n", replaced)	

def dict_to_markdown(d):
	code = d["code"]
	text = f'# {d["name"]}\n\n'
	if d["board"]:
		text += f'## The Board\n---\n{renderString(d["board"], code)}\n\n'
	if d["pieces"]:
		text += f'## The Pieces\n{renderString(d["pieces"], code)}\n\n'

	if d["tomove"] or d["towin"] or d["rules"]:
		text += f'## Rules\n'
	if d["tomove"]:
		text += f'**To Move:** {renderString(d["tomove"], code)}\n\n'
	if d["towin"]:
		text += f'**To Win:** {renderString(d["towin"], code)}\n\n'
	if d["rules"]:
		text += f'{renderString(d["rules"], code)}\n\n'

	if d["strategies"]:
		text += f'## Strategies\n'
		for d1 in d["strategies"]:
			for k, v in d1.items():
				text += f'- **{k}:** {renderString(v, code)}\n'
		text += '\n'

	if d["variants"]:
		text += f'## Variants\n'
		for d1 in d["variants"]:
			for k, v in d1.items():
				text += f'- **{k}**: {renderString(v, code)}\n'
		text += '\n'

	if d["history"]:
		text += f'## History\n{renderString(d["history"], code)}\n\n'

	if d["links"]:
		text += f'## Links\n\n'
		for d1 in d["links"]:
			for k, v in d1.items():
				text += f' - [{v}]({k})\n'
		text += '\n'

	if d["references"]:
		text += f'## References\n\n'
		for r in d['references']:
			text += f' - {r}\n'
		text += '\n'

	if d["gamescrafters"]:
		text += f'## GamesCrafters\n\n'
		for g in d['gamescrafters']:
			text += f' - {g}\n'

	return text


def read_from_file(game_id):
	with open(f'./xmlfiles/{game_id}.md', 'r') as reader:
		content = reader.read()
		d = convert_xml_dict(content)
		print(dict_to_markdown(d))


def md_instr(game_id, type='games', language='eng'):
	language = locale_map.get(language, language)
	link = f"http://gamescrafters.berkeley.edu/instructions/{language}/{type}/{game_id}.xml"
	instructions = read_from_link(link)
	if not instructions and language != 'eng':
		link = f"http://gamescrafters.berkeley.edu/instructions/eng/{type}/{game_id}.xml"
		instructions = read_from_link(link)
	return instructions


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	read_from_link('http://gamescrafters.berkeley.edu/games/1210.xml')
	print('---------------------------------------------------------\n')
	read_from_link('http://gamescrafters.berkeley.edu/games/baghchal.xml')