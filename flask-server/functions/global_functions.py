# -----------------------
# --  Global Functions --
# -----------------------

def allowed_file(filename, allowed_extensions):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in allowed_extensions

def safe_divide(n, d):
	# Safe division - return 0 if dividing by 0
	return n/d if d else 0