set "configs= berliand_berliand bignami clark hastenrath_lamb josey1 josey2 ssrd_strd ssrd_str ssr_strd ssr_str"

for %%x in (%configs%) do (
   echo %%x
   gotm gotm_%%x.yaml
)
