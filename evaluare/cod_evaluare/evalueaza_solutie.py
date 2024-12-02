def compare_annotations_position_token(filename_predicted,filename_gt,verbose=0):
	p = open(filename_predicted,"rt")  	
	gt = open(filename_gt,"rt") 

	
	line_gt = gt.readline()
	current_pos_gt, current_token_gt = line_gt.split()
	if verbose:
		print(current_pos_gt,current_token_gt)
	
	line_p = p.readline()
	current_pos_p, current_token_p = line_p.split()
	if verbose:
		print(current_pos_p,current_token_p)

	
	match_positions = 1
	match_tokens = 1
	if(current_pos_p != current_pos_gt):
		match_positions = 0
	if(current_token_p != current_token_gt):
		match_tokens = 0
	

	points_positions = 0.025 * match_positions
	points_tokens = 0.01 * match_tokens	


	return points_positions, points_tokens

#change this on your machine pointing to your results (txt files)
predictions_path_root = "../fisiere_solutie/463_Ionescu_Mircea/"
#predictions_path_root = "../fisiere_solutie/331_Alexe_Bogdan/"

#change this on your machine to point to the ground-truth test
gt_path_root = "fake_test_gt/"



def compare_annotations_score(filename_predicted,filename_gt,verbose=0):
	p = open(filename_predicted,"rt")  	
	gt = open(filename_gt,"rt") 

	all_lines_gt = gt.readlines()
	all_lines_p = p.readlines()


	number_lines_gt = len(all_lines_gt)

	points_scores = 0

	try:
		for i in range(0,number_lines_gt):
			line_gt = all_lines_gt[i]
			line_p = all_lines_p[i]
			if (line_gt==line_p):
				points_scores += 0.04
	except:
		pass

	return points_scores


#change this to 1 if you want to print results at each turn
verbose = 1
total_points = 0
for game in range(1,2):
# change this for game in range(1,5):
	points_score = 0
	for turn in range(1,51):
		
		name_turn = str(turn)
		if(turn < 10):
			name_turn = '0'+str(turn)

		filename_predicted = predictions_path_root + str(game) + '_' + name_turn + '.txt'
		filename_gt = gt_path_root + str(game) + '_' + name_turn + '.txt'

		game_turn = str(game) + '_' + name_turn
		points_position = 0
		points_tokens = 0	

		try:
			points_position, points_tokens  = compare_annotations_position_token(filename_predicted,filename_gt,verbose)
		except:
			print("Pentru imaginea: ", game_turn, " functia de evaluare a intampinat o eroare")

		print("Imaginea: ", game_turn, "Puncte task 1: ", points_position, "Puncte task 2: ",points_tokens)
		
		total_points = total_points + points_position + points_tokens

	filename_predicted_scores = predictions_path_root + str(game) + '_scores' + '.txt'
	filename_gt_scores = gt_path_root + str(game) + '_scores' + '.txt'
	points_score = compare_annotations_score(filename_predicted_scores,filename_gt_scores,verbose=0)
	print("Puncte task 3 ", points_score)

	total_points = total_points + points_score
	print("Total puncte = ", total_points)


print(total_points)
