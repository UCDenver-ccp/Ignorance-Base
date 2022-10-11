#!/usr/bin/env bash

original_article_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/1_First_Full_Annotation_Task_9_13_19/Articles/'


ignorance_base_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/3_Ignorance_Base/'
ignorance_folders='Ignorance-Base/Automated_Data_Corpus/'
articles='Articles/'

declare -a gold_standard_articles=('PMC6000839' 'PMC3800883' 'PMC2885310' 'PMC4311629' 'PMC3400371' 'PMC4897523' 'PMC3272870' 'PMC3313761' 'PMC3342123' 'PMC3427250' 'PMC4653418' 'PMC3279448' 'PMC6011374' 'PMC5812027' 'PMC2396486' 'PMC3915248' 'PMC3933411' 'PMC5240907' 'PMC4231606' 'PMC5539754' 'PMC5226708' 'PMC5524288' 'PMC3789799' 'PMC5546866' 'PMC5405375' 'PMC2722583' 'PMC1247630' 'PMC1474522' 'PMC2009866' 'PMC4428817' 'PMC5501061' 'PMC6022422' 'PMC1533075' 'PMC1626394' 'PMC2265032' 'PMC2516588' 'PMC2672462' 'PMC2874300' 'PMC2889879' 'PMC2898025' 'PMC2999828' 'PMC3205727' 'PMC3348565' 'PMC3373750' 'PMC3513049' 'PMC3679768' 'PMC3914197' 'PMC4122855' 'PMC4304064' 'PMC4352710' 'PMC4377896' 'PMC4500436' 'PMC4564405' 'PMC4653409' 'PMC4683322' 'PMC4859539' 'PMC4954778' 'PMC4992225' 'PMC5030620' 'PMC5143410' 'PMC5187359' 'PMC5273824' 'PMC5540678' 'PMC5685050' 'PMC6029118' 'PMC6033232' 'PMC6039335' 'PMC6054603' 'PMC6056931' 'PMC2722408' 'PMC2727050' 'PMC2913107' 'PMC3075531' 'PMC3169551' 'PMC3271033' 'PMC3424155' 'PMC3470091' 'PMC3659910' 'PMC3710985' 'PMC3828574' 'PMC4037583' 'PMC4275682' 'PMC4327187' 'PMC4380518' 'PMC4488777' 'PMC4715834' 'PMC4973215' 'PMC5340372' 'PMC5439533' 'PMC5658906' 'PMC5732505')

file_ext='.nxml.gz.txt'

##moving articles except for these
found=false
for file in $original_article_path/*
do
#    echo $file
    found=false

    for f in "${gold_standard_articles[@]}"
    do
#        echo $f

         if [[ "$file" == *"$f"* ]]
         then
            echo $f
            found=true
            break
         fi
    done


    if [[ "$found" == true ]]
    then
        echo "gold standard file"

    else
        cp $file $ignorance_base_path$ignorance_folders$articles
    fi



done

