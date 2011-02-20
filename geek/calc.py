def hash_rcn_phone(rcn=0, phone=0):
	hashkey = "BUZY92786PHVNDSGJFTWQRKCAME45X3"
	sharelist = []
	bignumber = rcn + phone
	for p in range(8, -1, -1):
		spot = int(bignumber / 31**p)
		decode = hashkey[spot]
		sharelist.append(decode)
		bignumber = bignumber - (spot * 31**p)
	sharecode = "".join(sharelist)
	return sharecode


def build_brickwall(wall):
	BRICKWIDTH=120
	BRICKS_PER_ROW=4
	
	brickcount = len(wall)
	brickrows, bricksleft = divmod(brickcount, BRICKS_PER_ROW)
	
	#brickrows = int(brickcount / BRICKS_PER_ROW)
	#bricksleft = brickcount - (brickrow * BRICKS_PER_ROW)
	
	# half row equals a row
	if (bricksleft > 0):
		brickrows = brickrows + 1
		
	looprows = reverse(enumerate(brickrows))	# should map to a list [27, 26, 25, . . . ,0]
	loopcols = enumerate(BRICKS_PER_ROW)		# should map to a list [0, 1, 2, etc. ]

	for row in looprows:
		for col in loopcols:
			brick = row * BRICKS_PER_ROW + col
			whocares, odd = divmod(row, 2)
			# if odd then start with a half brick
			if (odd):			
				if (col == 0):
					print "<td width=BRICKWIDTH colspan=1></td>"
				print "<td width=BRICKWIDTH colspan=2>%s %s %d</td>" % wall[brick].first_name, wall[brick].last_name, brick
			# if even, then end with a half brick
			else:
				print "<td width=BRICKWIDTH colspan=2>%s %s %d</td>" % wall[brick].first_name, wall[brick].last_name, brick
	
	
