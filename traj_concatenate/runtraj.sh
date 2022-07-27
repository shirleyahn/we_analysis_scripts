while read f; do
  iter=$(echo $f | awk '{print $1}')
  segid=$(echo $f | awk '{print $2}')
  echo $iter, $segid
  sed -i s"/ITER/${iter}/"g traj.sh
  sed -i s"/SEG/${segid}/"g traj.sh
  ./traj.sh
  sed -i s"/siter=${iter}/siter=ITER/"g traj.sh
  sed -i s"/sseg=${segid}/sseg=SEG/"g traj.sh
done < up_pathways.txt
