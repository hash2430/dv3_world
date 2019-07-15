# Generate experiments/s2/acoustic_model/data/file_id_list.scp from 
mgc_dir=./database/feats/mgc
out_file=./experiments/s2/acoustic_model/data/file_id_list.scp

if [ -f $out_file ]
then
	rm $out_file
fi

for file in $(ls $mgc_dir)
do
    echo $file | cut -d'.' -f1 >> $out_file
done
