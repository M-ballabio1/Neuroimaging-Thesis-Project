#! /bin/bash

#bl login

###################################################################################################################
######### 	Functions
###################################################################################################################

function Usage {
    cat <<USAGE
    
Usage:
` basename $0 ` -i <sbj_id> -p <project> [-t <t1.ext>] [-s <parc.ext>] [-a <affine.ext>] [-m <mask>] [-l <label.json>] [-g <tag>]
Compulsory arguments:
    
	-i, --sbj-id        subject id    
	-p, --project       project unique identifier 
Optional input:
	
	-g, --tag           tag
	-t, --t1            t1-w file fullpath
	-a, --affine        affine matrix file fullpath
	-m, --mask          brain mask file fullpath
	-s, --parc          parcellation or segmentation file fullpath
	-l, --label         label description json file fullpath (mandatory if --parc is given as input)
 
USAGE
    exit 1

}



###################################################################################################################
######### 	Input Parsing
###################################################################################################################

tag=''

# Provide output for Help
if [[ "$1" == "-h" || "$1" == "--help" ]];
  then
    Usage >&2
  fi

nargs=$#

if [ $nargs -lt 2   ];
  then
    Usage >&2


  fi



# As long as there is at least one more argument, keep looping
while [[ $# -gt 0 ]]; do
    key="$1"
    case "$key" in
        
        -h|--help)        
        Usage >&2
      	exit 0
        ;;    
        -i|--sbj-id)
        shift
        subj=${1}
        let nargs=$nargs-1
        ;;
        --sbj-id=*)
        subj="${key#*=}"
        ;;    
        -a|--affine)
        shift
        affine=${1}
        let nargs=$nargs-1
        ;;
        --affine=*)
        affine="${key#*=}"
        ;;
        -m|--mask)
        shift
        mask="${1}"
        let nargs=$nargs-1
        ;;
        --mask=*)
        mask="${key#*=}"
        ;;
        -s|--parc)
        shift
        parc="${1}"
        let nargs=$nargs-1
        ;;
        --parc=*)
        parc="${key#*=}"
        ;;        
        -p|--project)
        shift
        project="${1}"
        let nargs=$nargs-1
        ;;
        --project=*)
        project="${key#*=}"
        ;;
        -l|--label)
        shift
        label="${1}"
        let nargs=$nargs-1
        ;;
        --label=*)
        label="${key#*=}"
        ;; 
        -g|--tag)
        shift
        tag="${1}"
        let nargs=$nargs-1
        ;;
        --tag=*)
        tag="${key#*=}"
        ;;  
        -t|--t1)
        shift
        t1="${1}"
        let nargs=$nargs-1
        ;;
        --t1=*)
        t1="${key#*=}"
        ;;       
        *)
        # extra option
        echo "Unknown option '$key'"
        ;;
    esac
    # Shift after checking all the cases to get the next option
    shift
done

###################################################################################################################
######### 	MAIN
###################################################################################################################


	[ -z ${tag} ] || { tag_cmd='--tag '${tag} ; }

	[ -z ${project} ] && { project='60a14ca503bcad0ad27cada9' ; }

	#key='/home/gamorosino/data/Brain_Manual_Segmentation/key.txt'
	#label='/home/gamorosino/data/Brain_Manual_Segmentation/label.json'
	#cp ${seg} $( dirname ${seg} )'/parc.nii.gz'
	#parc=$( dirname ${seg} )'/parc.nii.gz'
	
	if ! [ -z ${t1}  ]; then 
		bl data upload --project ${project} --datatype "neuro/anat/t1w"				--subject ${subj} --t1 ${t1} ${tag_cmd}
	fi
	
	if ! [ -z ${mask}  ]; then 
		bl data upload --project ${project} --datatype "neuro/mask" 				--subject ${subj} --mask ${mask} ${tag_cmd} 
	fi
	
	if ! [ -z ${affine}  ]; then 
		bl data upload --project ${project} --datatype "neuro/transform"			--subject ${subj} --affine ${affine} ${tag_cmd}  --datatype_tag "linear"
	fi
	
	if ! [ -z ${parc}  ]; then	
		bl data upload --project ${project} --datatype "neuro/parcellation/volume"  --subject ${subj} --parc ${parc}  --label ${label} ${tag_cmd} 
	fi
