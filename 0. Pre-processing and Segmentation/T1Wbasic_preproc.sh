if [ $# -lt 1 ]; then							# usage dello script							
	    usage: "$( basename ${0} ) <imm_input.ext> [<num_cores>]"		
	    exit 1
fi

input_=$1


exists () {
                ############# ############# ############# ############# ############# ############# #############
                #############  		      Controlla l'esistenza di un file o directory	    ############# 
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


[ -z $num_cores ] && { num_cores=2; }

OMP_NUM_THREADS=${num_cores}
ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=${num_cores} 										
export OMP_NUM_THREADS
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS 

dim=3
		
input_N4=$( remove_ext $input_	)"_N4.nii.gz"
[ $( exists $input_N4 ) -eq 0 ] && { N4BiasFieldCorrection -d ${dim} -i $input_ -o $input_N4 -v  ; }

input_N4_reo=$( remove_ext $input_N4	)"_reoriented.nii.gz"


template=${FSLDIR}'/data/standard/MNI152_T1_1mm.nii.gz'

reo_dir=$( dirname $input_N4_reo )'/Reg2MNI/'
basena=$( remove_ext $( basename $input_N4_reo ) )


iter=10000x1000x1000

ANTS			-d ${dim} \
    			-m CC[${template},${input_N4},1,4] \
			-o ${reo_dir}/${basena}_2MNI_ \
		     	-i 0 -v  \
		     	-r Gauss[3,0.5] \
		     	--number-of-affine-iterations ${iter} \
		     	--do-rigid
antsApplyTransforms \
		     	-d ${dim} \
		     	-i ${input_N4} \
		     	-o ${input_N4_reo} \
		     	-r ${template} \
		     	-t ${reo_dir}/${basena}_2MNI_Affine.txt \
 		     	-n BSpline
