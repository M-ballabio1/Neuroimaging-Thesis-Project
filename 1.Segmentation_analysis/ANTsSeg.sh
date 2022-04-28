#!bin\bash

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/
t1=${1}
TEMPLATE_FOLDER=${2}"/"
ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=${3}				# multi-threading (per le funzioni di ANTs)
segment_dir=${4}"/"
brain_mask=${5}

echo t1: ${1}
echo template: ${2}
echo threads ${3}
echo output dir: ${4}
[ -z ${brain_mask} ] || {  bmask_cmd="-z "${brain_mask}; echo brain mask: ${5} ; }
mkdir -p ${segment_dir}
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS
#export ANTSPATH=/usr/lib/ants/
for stage in 1 2 3;
	do
	
	bash ${script_dir}/antsCorticalThickness_custom.sh -d 3 \
	-a ${t1} \
	-e ${TEMPLATE_FOLDER}PTBP_T1_Head.nii.gz \
	-m ${TEMPLATE_FOLDER}PTBP_T1_BrainCerebellumProbabilityMask.nii.gz \
	-p ${TEMPLATE_FOLDER}Priors/priors%d.nii.gz \
	-f ${TEMPLATE_FOLDER}PTBP_T1_ExtractionMask.nii.gz \
	-t ${TEMPLATE_FOLDER}PTBP_T1_BrainCerebellum.nii.gz \
	-y ${stage} \
	-k 0 -n 3 -w 0.25 -q 0 \
	-o ${segment_dir} ${bmask_cmd}
	
done;


