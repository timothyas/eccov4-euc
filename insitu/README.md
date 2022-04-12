# Insitu data

## TAO Array

This command grabs sections that start with `#---` (etc) and end with
`END OF VARIABLES SECTION`, when `(TAO) BUOY ARRAY` is in between.
```bash
sed -n
'/#--------------------------------------------------------------------------------/!b;:a;/END
OF VARIABLES SECTION/!{$!{N;ba}};{/(TAO) BUOY ARRAY/p}'
ocldb1526349572.28401.MRB.csv > tao_data.txt
```

See `get_tao.sh`, note the following manual modifications, added to the bash
script
- Preprocessing: mv `MRB.csv` to `MRB1.csv` so they're all numbered..
- Postprocessing: the `MRB1.csv` file is the only one that has trouble with this
  `sed` command, because there are some items that have no T/S data  section,
  and so do not end with `END OF VARIABLES SECTION`. For some reason, the python
  script has a hard time getting the right line number on these (?), so have to
  manually edit the text file by first looking for the temperature/salinity
  values. This turns up a an item from `MONTEREY BAY`,
- Make sure find and replace `sed` command ends with `/g` in order to get all
  instances...

## TRITON Array

Same idea, but use the identifier `TRITON (TRIANGLE TRANS-OCEAN BUOY NETWORK)`.
See `get_triton.sh`.

### Location data only

To get just the location data from the csv files, use `grep`.
To just get the locations, run:

```bash
grep -B 8 "(TAO) BUOY ARRAY" MRB_CSV/*.csv > tao_location.txt
```


### None of these commands worked as well

```bash
grep -B 8 -A 50 "(TAO)" ocldb1526349572.28401.MRB.csv > tao_data.txt
```

better...

```bash
grep  --group-separator="#-#-#-#-#" -B 8 -A 50 "(TAO)" ocldb1526349572.28401.MRB.csv > tao_data.txt
```

```
awk '/#--------------------------------------------------------------------------------/ {p=1};
     {if (p==1) {a[NR]=$0}};
     /(TAO) BUOY ARRAY/ {f=1};
     /#--------------------------------------------------------------------------------/ {p=0; if (f==1) {for (i in a) print a[i]};f=0; delete a}' ocldb1526349572.28401.MRB.csv

```

Next to try...
```
sed -n '/Beginning of block/!b;:a;/End of block/!{$!{N;ba}};{/some_pattern/p}' filename
```
