set "configs= ssr_berliand_berliand ssr_bignami ssr_clark ssr_hastenrath_lamb ssr_josey1 ssr_josey2"

for %%x in (%configs%) do (
   echo %%x
   gotm gotm_%%x.yaml
)
