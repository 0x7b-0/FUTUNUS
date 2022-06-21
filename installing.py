import os
try:
	os.system('pip3 install pywifi')
	os.system('pip3 install comtypes')
	os.system('pip3 install rich')
except:
	print('Installing error!')
else:
	print("Installing comlete!")