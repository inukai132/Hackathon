def permission(class, lvl, f):
	file_cat_req = f.category	#file category requirement
	file_per_req = f.level		#file permission requiremnt
	if class != file_cat_req:
		return -1
	elif lvl < file_per_req:
		return -1
	else:
		return 0
def caller(class, lvl, f):
	if permission(class, lvl, f) == 0:
		print f
	else:
		print "Permission denied."
		
