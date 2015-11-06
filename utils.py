def colored54_to_perm48(s):
	"""
	La fonction va tranformer une chaine de caractère sous la forme (RGBW...) de la perm 54 en 48
	"""
	r = ""
	for i in range(0,len(s)):
		if i == 4:
			r = r + "U"
		elif i == 22:
			r = r + "L"
		elif i == 25:
			r = r + "F"
		elif i == 28:
			r = r + "R"
		elif i == 31:
			r = r + "B"
		elif i == 49:
			r = r + "D"
		else:
			r = r+s[i]
	return r

