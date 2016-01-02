"""
Check for installed packages
fyi, pip will install dependences
"""

import pip
import argparse
import os

parser = argparse.ArgumentParser(description='Print list of installed packages')

parser.add_argument('--find', nargs='+', metavar='PKG', help="check if specific PKG or PKGs are installed, PKG can be a string or list", action='store')

args = parser.parse_args()

installed_packages = pip.get_installed_distributions()
installed_packages_list = sorted(["{:}({:})".format(str.lower(i.key), i.version)
     for i in installed_packages])

if type(args.find) == list:
	chk = []
	for pkg in args.find:
		currchk = [s for s in installed_packages_list if str.lower(pkg) in s]
		if len(currchk) > 0:
			chk.extend(currchk)
		else:
			chk.append(pkg+' not found')
	[print(s) for s in chk]

elif type(args.find) == str:
	chk = [s for s in installed_packages_list if str.lower(args.find) in s]
	if not chk:
		print('Unable to find installed package',args.find)
	else:
		[print(s) for s in chk]

else:
# 	height, width = os.popen('stty size', 'r').read().split()
# 	cols = int(int(width)/32)
# 	fmtlist = []
# 	for i in range(cols):
# 		fmtlist.append(installed_packages_list[i::cols])
# 	for j in range(	
# 		for i in range(cols):
# 			curr = 
# 	[print('{:<32}'.format(fmtlist[:][i])) for i in range(cols)]
	odds = installed_packages_list[::2]
	evens = installed_packages_list[1::2]
	if len(odds) == len(evens):
		for odd,even in zip(odds, evens):
			print('{:<32}'.format(odd),'{:<32}'.format(even))
	else:
		evens.append('')
		for odd,even in zip(odds, evens):
			print('{:<32}'.format(odd),'{:<32}'.format(even))

print('Total installed pkgs:',len(installed_packages_list))
