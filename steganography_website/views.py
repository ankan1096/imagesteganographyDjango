from django.shortcuts import render
from .forms import EncodindForm, DecodingForm
from django.http import HttpResponseRedirect
import sys
import os
from tkinter import *
from tkinter.filedialog import *
from PIL import ImageTk
from PIL import Image as im
#from matplotlib import image as img
from numpy import array
from numpy import vectorize as vec
from numpy import binary_repr as binary
from numpy import dstack as ds
import cv2



def home(request):

	submitted = False
	if request.method == "POST":
		#encodingform = EncodindForm(request.POST)
		user_input = request.POST.get('user_input')
		secret_data_path = request.POST.get('secret_data_path')
		layer_choice = request.POST.get('layer_choice')
		stego_file_name = request.POST.get('stego_file_name')
		file_location = request.POST.get('file_location')


		size_image_file = os.path.getsize(user_input)
		size_secretdata_file = os.path.getsize(secret_data_path)
		stego_ratio = size_secretdata_file / size_image_file

		assert os.path.exists(user_input), "I did not find the file at, "+str(user_input)
		secret_data = open(secret_data_path,'r+')

		#performs encoding using LSB technique

		image = im.open(user_input)
		arr = array(image)
		secret_content = secret_data.read()
		secret_data.close()

		red, green, blue = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]


		if(layer_choice.lower() == 'red' or layer_choice.lower() == 'r'):
			binary_rep = vec(binary)
			binary_array_rgb = binary_rep(red, 8)
		elif(layer_choice.lower() == 'green' or layer_choice.lower() == 'g'):
			binary_rep = vec(binary)
			binary_array_rgb = binary_rep(green, 8)
		elif(layer_choice.lower() == 'blue' or layer_choice.lower() == 'b'):
			binary_rep = vec(binary)
			binary_array_rgb = binary_rep(blue, 8)


		length_secret_text = len(secret_content)
		length_secret_text_binary = bin(length_secret_text).replace('0b', '')
		temp = length_secret_text_binary[::-1]
		while len(temp) < 32:
			temp += '0'
		length_secret_text_binary = temp[::-1]
		ascii_values = [ord(character) for character in secret_content]
		ascii_values_binary = binary_rep(ascii_values, 8)

		row = 0
		column = -1

		#Here Last 4 bits are used to hide the secret information
		#First 32 bits are used to store the length of the data

		for index in range(0, 32, 4):
			if column == len(binary_array_rgb[0]) - 1:
				row = row + 1
				column = 0
			else:
				column = column + 1
			pixel_binary_value = binary_array_rgb[row][column]
			if length_secret_text_binary[index : index + 4] == '0000':
				pixel_binary_value = pixel_binary_value[:4] + '0000' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '0001':
				pixel_binary_value = pixel_binary_value[:4] + '0001' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '0010':
				pixel_binary_value = pixel_binary_value[:4] + '0010' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '0011':
				pixel_binary_value = pixel_binary_value[:4] + '0011' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '0100':
				pixel_binary_value = pixel_binary_value[:4] + '0100' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '0101':
				pixel_binary_value = pixel_binary_value[:4] + '0101' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '0110':
				pixel_binary_value = pixel_binary_value[:4] + '0110' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '0111':
				pixel_binary_value = pixel_binary_value[:4] + '0111' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '1000':
				pixel_binary_value = pixel_binary_value[:4] + '1000' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '1001':
				pixel_binary_value = pixel_binary_value[:4] + '1001' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '1010':
				pixel_binary_value = pixel_binary_value[:4] + '1010' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '1011':
				pixel_binary_value = pixel_binary_value[:4] + '1011' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '1100':
				pixel_binary_value = pixel_binary_value[:4] + '1100' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '1101':
				pixel_binary_value = pixel_binary_value[:4] + '1101' + pixel_binary_value[8:]
			elif length_secret_text_binary[index : index + 4] == '1110':
				pixel_binary_value = pixel_binary_value[:4] + '1110' + pixel_binary_value[8:]
			else:
				pixel_binary_value = pixel_binary_value[:4] + '1111' + pixel_binary_value[8:]
			binary_array_rgb[row][column] = pixel_binary_value

		#Remaining bits are used to hide the original data

		for val in ascii_values_binary:
			num = val
			idx = 0
			while idx != 8:
				if column == len(binary_array_rgb[0]) - 1:
					row = row + 1
					column = 0
				else:
					column = column + 1
				pixel_binary_value = binary_array_rgb[row][column]
				if num[idx : idx + 4] == '0000':
					pixel_binary_value = pixel_binary_value[:4] + '0000' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '0001':
					pixel_binary_value = pixel_binary_value[:4] + '0001' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '0010':
					pixel_binary_value = pixel_binary_value[:4] + '0010' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '0011':
					pixel_binary_value = pixel_binary_value[:4] + '0011' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '0100':
					pixel_binary_value = pixel_binary_value[:4] + '0100' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '0101':
					pixel_binary_value = pixel_binary_value[:4] + '0101' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '0110':
					pixel_binary_value = pixel_binary_value[:4] + '0110' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '0111':
					pixel_binary_value = pixel_binary_value[:4] + '0111' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '1000':
					pixel_binary_value = pixel_binary_value[:4] + '1000' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '1001':
					pixel_binary_value = pixel_binary_value[:4] + '1001' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '1010':
					pixel_binary_value = pixel_binary_value[:4] + '1010' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '1011':
					pixel_binary_value = pixel_binary_value[:4] + '1011' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '1100':
					pixel_binary_value = pixel_binary_value[:4] + '1100' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '1101':
					pixel_binary_value = pixel_binary_value[:4] + '1101' + pixel_binary_value[8:]
				elif num[idx : idx + 4] == '1110':
					pixel_binary_value = pixel_binary_value[:4] + '1110' + pixel_binary_value[8:]
				else:
					pixel_binary_value = pixel_binary_value[:4] + '1111' + pixel_binary_value[8:]
				binary_array_rgb[row][column] = pixel_binary_value
				idx = idx + 4


		if(layer_choice.lower() == 'red' or layer_choice.lower() == 'r'):
			for i in range(0, len(binary_array_rgb)):
				for j in range(0, len(binary_array_rgb[0])):
					red[i][j] = int(binary_array_rgb[i][j], 2)

		elif(layer_choice.lower() == 'green' or layer_choice.lower() == 'g'):
			for i in range(0, len(binary_array_rgb)):
				for j in range(0, len(binary_array_rgb[0])):
					green[i][j] = int(binary_array_rgb[i][j], 2)

		elif(layer_choice.lower() == 'blue' or layer_choice.lower() == 'b'):
			for i in range(0, len(binary_array_rgb)):
				for j in range(0, len(binary_array_rgb[0])):
					blue[i][j] = int(binary_array_rgb[i][j], 2)

		reconstructed_image = ds((red, green, blue))
		newImage = im.fromarray(reconstructed_image, "RGB")
		newImage.save(f"{file_location}/{stego_file_name}.png")

		#return HttpResponseRedirect('/?submitted=True')
		return render(request, 'processcompleted.html', {'type' : False, 'stego_file_name' : stego_file_name, 'file_location' : file_location, 'size_image_file' : size_image_file, 'size_secretdata_file' : size_secretdata_file, 'stego_ratio' : stego_ratio})
	else:
		encodingform = EncodindForm
		decodingform = DecodingForm
		#if 'submitted' in request.GET:
			#submitted = True

		#print(user_input+" "+secret_data_path+" "+layer_choice+" "+stego_file_name+" "+file_location+" "+str(stego_ratio))
		#sys.stdout.flush()

	
	return render(request, 'home.html', {'encodingform' : encodingform, 'submitted' : submitted, 'decodingform' : decodingform})

def about(request):
	return render(request, 'about.html', {})

def processcompleted(request):


	user_input = request.POST.get('user_input')
	layer_choice = request.POST.get('layer_choice')
	stego_file_name = request.POST.get('stego_file_name')
	file_location = request.POST.get('file_location')

	assert os.path.exists(user_input), "I did not find the file at, "+str(user_input)
	image = im.open(user_input)
	arr = array(image)

	red, green, blue = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

	if(layer_choice.lower() == 'red' or layer_choice.lower() == 'r'):
		binary_rep = vec(binary)
		binary_array_rgb = binary_rep(red, 8)
	elif(layer_choice.lower() == 'green' or layer_choice.lower() == 'g'):
		binary_rep = vec(binary)
		binary_array_rgb = binary_rep(green, 8)
	elif(layer_choice.lower() == 'blue' or layer_choice.lower() == 'b'):
		binary_rep = vec(binary)
		binary_array_rgb = binary_rep(blue, 8)


	length_secret_text_binary = ''
	row = 0
	column = -1

	#Length Of The Secret Data Is Retrieved
	for index in range(0, 32, 4):
		if column == len(binary_array_rgb[0]) - 1:
			row = row + 1
			column = 0
		else:
			column = column + 1
		pixel_binary_value = binary_array_rgb[row][column]
		length_secret_text_binary = length_secret_text_binary + pixel_binary_value[4 : 8]

	length_secret_text = int(length_secret_text_binary, 2)

	#Secret Data Is Retrieved
	secret_text = ''
	for index in range(length_secret_text):
		secret_character_ascii_value_binary = ''
		for count in range(0, 8, 4):
			if column == len(binary_array_rgb[0]) - 1:
				row = row + 1
				column = 0
			else:
				column = column + 1
			pixel_binary_value = binary_array_rgb[row][column]
			secret_character_ascii_value_binary = secret_character_ascii_value_binary + pixel_binary_value[4 : 8]
		secret_character_ascii_value = int(secret_character_ascii_value_binary, 2)
		secret_text = secret_text + chr(secret_character_ascii_value)


	completeName = os.path.join(file_location, stego_file_name + ".txt")
	file1 = open(completeName, "w")
	file1.write(secret_text)
	file1.close()


	#print(user_input+" "+layer_choice+" "+stego_file_name+" "+file_location)
	#sys.stdout.flush()
	return render(request, 'processcompleted.html', {'type' : True, 'stego_file_name' : stego_file_name, 'file_location' : file_location})