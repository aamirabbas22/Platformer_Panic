from settings import * # Import global constants/settings
from os import walk # walk() lets you iterate through directories
from os.path import join # join() combines paths in an OS-safe way

def import_image(*path, alpha = True, format = 'png'):
	full_path = join(*path) + f'.{format}' # Build full file path 
	if alpha:
		return pygame.image.load(full_path).convert_alpha() # Load with transparency
	else:
	    return pygame.image.load(full_path).convert()  # Load without alpha channel

def import_folder(*path):
	frames = []
	for folder_path, subfolders, image_names in walk(join(*path)):
		for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
			full_path = join(folder_path, image_name)
			frames.append(pygame.image.load(full_path).convert_alpha())
	return frames # Return list of image surfaces

def import_folder_dict(*path):
	frame_dict = {}
	for folder_path, _, image_names in walk(join(*path)):
		for image_name in image_names:
			full_path = join(folder_path, image_name)
			surface = pygame.image.load(full_path).convert_alpha()
			frame_dict[image_name.split('.')[0]] = surface 
	return frame_dict

def import_sub_folders(*path):
	frame_dict = {}
	for _, sub_folders, __ in walk(join(*path)): 
		if sub_folders:
			for sub_folder in sub_folders:
				# Recursively load all images in each subfolder
				frame_dict[sub_folder] = import_folder(*path, sub_folder)
	return frame_dict