pd=read_csv=....

sb_id_v=dp[0].values
tag_1_v=dp[1].values
tag_2_v=dp[2].values
tag_3_v=dp[3].values


t1_condi_v=dp[6].values
seg_condi_v=dp[7].values
mask_cond_v=dp[8].values
aff_cond_v=dp[9].values

path_data=/home/matteto..../DBB_dataset/
images_pah=path_data+/images/
mask_pah=path_data+/raw_masks/

label_file=path_data+'/info/label.json

project='60a14ca503bcad0ad27cada9'


for i in range(len(sbj_di_v)):


	sbj_id_i=sb_id_v[i]

	command0=' -i '+sbj_id_i


	seg_name=sbj_id_i.replace('sub-','SEGMENATATION_')
	seg_file=images_pah+seg_name+'nii.gz'	
	commandseg=' bl data upload --project '+project+' --datatype "neuro/parcellation/volume"  --subject '+subj+' --parc '+seg_file+'  --label '+label+' --tag '+tag1+' --tag '+tag2+' --tag '+tag3
	os.system(commandseg)


	tag1=tag_1_v[i]
	tag2=tag_2_v[i]
	tag3=tag_3_v[i]

	if t1_condi_v[i] == 'YES':
		file_t1_name=sbj_id_i.replace('sub-','IMAGE_')
		file_t1=images_pah+file_t1_name+'nii.gz'

		commandt1='bl data upload --project ${project} --datatype "neuro/anat/t1w"				--subject ${subj} --t1 ${t1} ${tag_cmd}'+' --tag '+tag1+' --tag '+tag2+' --tag '+tag3
		os.system(commandt1)		


	if mask_cond_v[i] == 'YES':
		mask_name=sbj_id_i.replace('sub-','IMAGE_')
		mask_t1=images_pah+file_t1_name+'nii.gz'
		commandm='bl data upload --project ${project} --datatype "neuro/mask" 				--subject ${subj} --mask ${mask} ${tag_cmd} '+' --tag '+tag1+' --tag '+tag2+' --tag '+tag3
		os.system(commandm)

	if affine_cond_v[i] == 'YES':
		aff_name=sbj_id_i.replace('sub-','BRAINA_MASK_')
		afff_t1=mask_path+file_t1_name+'nii.gz'
		
		command2='bl data upload --project ${project} --datatype "neuro/transform"			--subject ${subj} --affine ${affine} ${tag_cmd}  --datatype_tag "linear"'+' --tag '+tag1+' --tag '+tag2+' --tag '+tag3

		os.system(command2)

