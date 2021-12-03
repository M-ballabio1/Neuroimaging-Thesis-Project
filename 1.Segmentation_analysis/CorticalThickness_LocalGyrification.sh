#!/bin/bash
# Cortical thickness, surface area, and curvature estimates
# for individual subjects
#
################################################################
#The explanations of the meaning of all parameters of command SurfaceCurvature are contained in:
#
#  Avants B., Gee J. (2003) The Shape Operator for Differential Analysis of Images. In: Taylor C., 
#  Noble J.A. (eds) Information Processing in Medical Imaging. IPMI 2003. Lecture Notes in Computer Science, 
#  vol 2732. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-540-45087-0_9
#
#Parameters explanation:
#SURFACE CURVATURE:
#
#The first parameter indicates most likely a level of smoothing where 0 = min and 7 = max
#The second parameter indicates different results. Infact, 0 = Mean Curvature 6 = Gauss Curvature 7 = Surface Area
#
################################################################

source_folder=${1}
cortical_dir=${2}
surface_dir=${3}
ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=${4}

if [ "$#" == "0" ]; then
        echo " usage: "
        echo "       "$( basename ${0} )" <segmentations_folder> <Output_Cortical_folder> <Output_Surface_folder> <threads>"
        echo "  "
        echo "  dependencies: "
        echo "          ANTs "
        echo "          CorticalThickness_LocalGyrification.sh "
        echo "   "
        echo "  # CorticalThickness_LocalGyrification_subject_ pipeline:
                # 1. Cortical thickness estimation with Segmentation Complete mask as a prior using KellyKapowski
                # 2. Surface area and curvature estimation using SurfaceCurvature over Segmentation Complete mask "
        echo "          "
        echo "  "
        exit
fi

[ -z ${ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS}  ] && { ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=1 ; }

[ -z ${cortical_dir}  ] && { cortical_dir=$( dirname $T1w )"/AntsSegmentation/" ; }
mkdir -p $segment_dir
[ -z ${segment_dir}  ] && { segment_dir=$( dirname $T1w )"/AntsSegmentation/" ; }
mkdir -p $segment_dir

echo "Segmentations Complete: ${1}"
echo "Cortical dir: ${2}"
echo "Surface Dir: ${3}"
echo "Num THREADS: ${4}"

counter=0
for FILE in $(ls $source_folder/*.gz ) ;
  do
    BFILE=$(basename $FILE )

# Cortical thickness estimation

$ANTSPATH/KellyKapowski -d 3 -s $(basename)_Segmentazione_Completa.nii.gz -t 5 -o $(basename)_Cortical_Thickness.nii.gz -v 1

# Surface area estimation

$ANTSPATH/SurfaceCurvature $(basename)_Segmentazione_Completa.nii.gz $cortical_dir"/SurfaceArea.nii.gz" 0 7

# Mean and intrinsic (Gaussian) curvature estimation

$ANTSPATH/SurfaceCurvature ${basename}_Segmentazione_Completa.nii.gz $surface_dir"/MeanCurv.nii.gz" 0 0
$ANTSPATH/SurfaceCurvature ${basename}_Segmentazione_Completa.nii.gz $surface_dir"/GaussCurv.nii.gz" 0 6
  done
