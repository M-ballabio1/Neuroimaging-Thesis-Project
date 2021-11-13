#! /bin/bash


###################################################################################################################
######### 	Functions
###################################################################################################################

function Usage {
    cat <<USAGE
    
Usage:
` basename $0 ` -i <T1.ext> -t <template.ext> [-o <outputdir>] [-a <affine.ext>] [-m <mask.ext>] [-n <num>]
Main arguments:
    
	-i, --input         T1-w image to be preprocessed    
	-t, --template      template as reference space to be reoriented
   
General Options:
	-o, --outputdir     if not provided, the scripts create the folder 
	-a, --affine        affine matrix to perform rigid transformation to the template
	-m, --mask          brain mask to limit Bias-field correction on these voxels     
	-n, --nthreads      number of threads      	
 
USAGE
    exit 1

}

exists () {
   
                ############# ############# ############# ############# ############# ############# #############
                ##############  	  Check existence of a file or directory                        ############# 
                ############# ############# ############# ############# ############# ############# #############  		
                      			
		if [ $# -lt 1 ]; then
		    echo $0: "usage: exists <filename> "
		    echo "    echo 1 if the file (or folder) exists, 0 otherwise"
		    return 1;		    
		fi 
		
		if [ -d "${1}" ]; then 

			echo 1;
		else
			([ -e "${1}" ] && [ -f "${1}" ]) && { echo 1; } || { echo 0; }	
		fi		
		};


remove_extx () {
	
	local result=$( echo ` basename $1 | cut -d '.' -f 1 ` )
	local extension="${result##*.}"
	if [ "${extension}" == "nii" ]; then
		local result=$( echo ` basename $result | cut -d '.' -f 1 ` )	
	fi 
	
	echo ${result}
	
	
}

###################################################################################################################
######### 	Input Parsing
###################################################################################################################

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
        -i|--input)
        shift
        input_=${1}
        let nargs=$nargs-1
        ;;
        --input=*)
        input_="${key#*=}"
        ;;    
        -t|--template)
        shift
        template=${1}
        let nargs=$nargs-1
        ;;
        --template=*)
        template="${key#*=}"
        ;; 
        -o|--outputdir)
        shift
        outputdir=${1}
        let nargs=$nargs-1
        ;;
        --outputdir=*)
        outputdir="${key#*=}"
        ;;
        -a|--affine)
        shift
        affine="${1}"
        let nargs=$nargs-1
        ;;
        --affine=*)
        affine="${key#*=}"
        ;;
        -m|--mask)
        shift
        T1_mask="${1}"
        let nargs=$nargs-1
        ;;
        --mask=*)
        T1_mask="${key#*=}"
        ;;
        -n|--nthreads)
        shift 
        nthreads="$1"
        let nargs=$nargs-1
        ;;
        --nthreads=*)
        nthreads="${key#*=}"
        ;;
        -f|--force)        
		force=1	
        ;;
        -v|--verbose)        
		verbose=1	
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
######### 	Set number of threads
###################################################################################################################

[ -z $nthreads ] && { nthreads=2; }

OMP_NUM_THREADS=${nthreads}
ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=${nthreads} 										
export OMP_NUM_THREADS
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS 


###################################################################################################################
######### 	Reorientation
###################################################################################################################



dim=3

#template=${FSLDIR}'/data/standard/MNI152_T1_1mm.nii.gz'

if [ -z ${outputdir} ]; then
	outputdir=$( dirname $input_ )'/T1w_preproc/'
fi

basena=$( remove_extx $( basename $input_ ) )
if [ -z ${affine} ]; then
	affine=${outputdir}/${basena}_2MNI_Affine.txt
fi

if [ -n "${T1_mask}" ]; then
	mask_opt=" -x ${T1_mask} "
fi


[ -d ${outputdir} ] || { mkdir ${outputdir} ; }


input_reo=${outputdir}'/'$( remove_extx $input_	)"_reoriented.nii.gz"

if [ $( exists $input_reo ) -eq 0 ]; then

	if [ $( exists ${affine} ) -eq 0 ]; then

		iter=10000x1000x1000

		ANTS			3 -m CC[${template},${input_},1,4] \
						-o ${outputdir}/${basena}_2MNI_ \
						-i 0 -v  \
						-r Gauss[3,0.5] \
						--number-of-affine-iterations ${iter} \
						--do-rigid
	fi

	if [ $( exists $input_reo ) -eq 0 ]; then
		antsApplyTransforms \
						-d ${dim} \
						-i ${input_} \
						-o ${input_reo} \
						-r ${template} \
						-t ${affine} \
						-n BSpline

	fi

fi
###################################################################################################################
######### 	Bias Field Correction
###################################################################################################################


		
input_N4=${outputdir}'/'$( remove_extx $input_reo	)"_N4.nii.gz"
if [ $( exists $input_N4 ) -eq 0 ]; then

	N4BiasFieldCorrection 	-d ${dim} \
							-i $input_reo \
							-o $input_N4 \
							-v ${mask_opt} ; 
fi
