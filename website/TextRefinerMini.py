def bullet(text, nl="python"):
	# a = "1.) x = 11/2 2.) e = 2"
	text = str(text)
	num = [1, 2, 3, 4, 5, 6, 7, 8, 9]

	if nl == "markup":
		for n in num:
			if f" {n}.)" in text:
				bulleted = (text.replace(f" {n}.)", f"<br>{n}.)"))
			elif f" {n})" in text:
				bulleted = (text.replace(f" {n})", f"<br>{n})"))

			elif f"\n{n}.)" in text:
				bulleted = (text.replace(f" {n}.)", f"<br>{n}.)"))
			elif f"\n{n})" in text:
				bulleted = (text.replace(f" {n})", f"<br>{n})"))

			else:
				bulleted = text
	else:
		for n in num:
			if f" {n}.)" in text:
				bulleted = (text.replace(f" {n}.)", f"\n{n}.)"))
			elif f" {n})" in text:
				bulleted = (text.replace(f" {n})", f"\n{n})"))

			elif f"\n{n}.)" in text:
				bulleted = (text.replace(f" {n}.)", f"\n{n}.)"))
			elif f"\n{n})" in text:
				bulleted = (text.replace(f" {n})", f"\n{n})"))

			else:
				bulleted = text
		

	return bulleted
	

def abbr(name, count=2):
	count = count - 1
	# name = "isaac"

	# count = 1

	n_list = []

	for n in name:
		n_list.append(n)

	return [((n_list[count-1] + n_list[count]).upper()), n_list]

# print(w)


# b = "monday tuesday wednesday thursday"
# for n in num:
# 	if " " in b:
# 		x = b.replace(" ", f"\n{n}.) ")

# print(x)