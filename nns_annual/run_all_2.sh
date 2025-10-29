GOTM=/home/kb/local/gcc/13/gotm/7/bin/gotm

configs="ssr_berliand_berliand ssr_bignami ssr_clark ssr_hastenrath_lamb ssr_josey1 ssr_josey2r"

for config in $configs; do
  echo $config
  $GOTM gotm_$config.yaml >&$config.log
done
