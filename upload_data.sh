#!/bin/bash


str_indices() {    
                
                ############# ############# ############# ############# ############# ############# 
                ############   Restituisce gli indice di una carattere in una stringa	########### 
                ############# ############# ############# ############# ############# #############         

		if [ $# -lt 2 ]; then							# usage dello script							
			    echo $0: "usage: str_index <string> <char> [<separator>]"
			    return 1;		    
		fi       

                local stringa=$1;
                local target=$2
                local sep=$3   
                local N=${#stringa}
				local conta=0
				local last_res=""
				local results=""
				[ -z $sep ] && { sep=","; }
				[ "${sep}" == "space" ] && { sep=" "; }
						for ((i=0;i<=N;i++)) do
							[ "${target}" == "${stringa:$i:1}" ] && \
							{ conta=$(( $conta + 1 ));results=${last_res}${sep}$i;last_res=$results; }
						done 
						echo "${results:1:${#results}}"
						};	



## MAIN

bl login

project=60a14ca503bcad0ad27cada9
T1_full=/home/matteo99/mnt/nilabserver/home/matteoballabio/mnt/data/all_subjects_processed/SUBJECT_segmentated/SUBJECT_COMPLETED/SUBJECT_T1W3D_ACPC_BIAS_DEFACED
#T1_brain=/home/matteo99/mnt/nilabserver/home/matteoballabio/mnt/data/all_subjects_processed/SUBJECT_segmentated/SUBJECT_COMPLETED/SUBJECT_T1W3D_BRAIN
#T1_mask=/home/matteo99/mnt/nilabserver/home/matteoballabio/mnt/data/all_subjects_processed/SUBJECT_segmentated/SUBJECT_COMPLETED/SUBJECT_SEGMENTATION_COMPLETED



for t1 in $(ls ${T1_full}/* -d ); do
		indices=( $( str_indices ${t1} '_' ))
        subject=${t1:0:${indices[1]}}
        bl data upload --project $project --datatype neuro/anat/t1w --subject $subject --t1 ${t1} --tag "defaced"
    
done
