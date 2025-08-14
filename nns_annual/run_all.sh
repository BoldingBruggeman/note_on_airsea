GOTM=/home/kb/local/gcc/13/gotm/7/bin/gotm

configs="berliand_berliand bignami clark hastenrath_lamb josey1 josey2 ssrd_strd ssrd_str ssr_strd ssr_str"

for config in $configs; do
  echo $config
  $GOTM gotm_$config.yaml >&$config.log
done
