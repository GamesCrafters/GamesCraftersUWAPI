import xml.etree.ElementTree as ET
import urllib.request
import re

"""
	By default, we use the XML files and images hosted on GitHub on the GamesCrafters
	Explainers Repo. Set `instructions_link` to...
	...the 1st link if you want to use the Explainers repo hosted on GitHub. (DEFAULT)
	...the 2nd link if you want to use the Explainers repo on your computer.
	...the 3rd link if you want to use the Explainers repo on gamescrafters.berkeley.edu.

	Note: Markdown has issues displaying local images when you don't set up a webserver for it,
	so if you decide to test what the Instructions look like on GamesmanUni and
	set `instructions_link` to the 2nd option, you'll be able to see the text
	but not the images. I suggest that you create a branch on the Explainers directory, 
	put your XML files and images there, then change `instructions_link` to point to that branch
	if you want to see what your images look like when the "i" button is clicked on Uni.
"""
instructions_link = "https://raw.githubusercontent.com/GamesCrafters/Explainers/master/instructions/"
#instructions_link = "file:///<PATH TO YOUR EXPLAINERS DIRECTORY>/Explainers/instructions/"
#instructions_link = "http://gamescrafters.berkeley.edu/instructions/"

instructions_text_link = instructions_link + '{}/{}/{}.xml'
instructions_images_directory_link = instructions_link + 'i/{}/'

locale_map = {
	'en-US': 'eng',
	'es': 'spa'
}

def read_from_link(url: str) -> str:
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
		return ''

def parse_list_items(bag, child, name) -> bool:
	if child.tag == name:
		bag[name] = []
		for r in child:
			bag[name].append(r.text)
		return True
	return False

def parse_nested(bag, child, name: str, key_tag: str = 'name', value_tag: str = 'description'):
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
	"""
		The first line uses images from gamescrafters.berkeley.edu.
		The second one uses images from GitHub.
		We link to images hosted on GitHub for the time being.
	"""
	replaced = re.sub(r"\[img\s+src\s*=\s*\"([^\"]*)\"([^\]]+)\]", '![alt](' + instructions_images_directory_link.format(code) + r'\1)', s)
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

def md_instr(game_type, game_id, language):
	language = locale_map.get(language, language)
	instructions = read_from_link(instructions_text_link.format(language, game_type, game_id))
	if not instructions and language != 'eng':
		instructions = read_from_link(instructions_text_link.format('eng', game_type, game_id))
	return instructions