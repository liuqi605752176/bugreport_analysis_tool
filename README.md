The bugreport analysis tool to sort bug report data

Usage:

buganalysis.py <options>  --file  bugreport.zip --out /tmp/test 

options:
	-h,--help		 						- print help
	-v,--verbose		 				- print verbose logging
	--file <filename>	 			- zip or txt file of bugreport
	--out <out_dir>		 			- output dir
	--bugid <bug number>	 	- Redmine bug number
	--bugtitle <bug title>	- Redmine bug title
	--dev <developer name>	- Developer name
	--tester <tester name>	- Test engineer name
	--eventbypid		 				- Filter event logs by pid
	--version		 						- print version



Examples:
python buganalysis.py -v --file bugreport-tphoneY-T5711INDURG-264-2018-07-30-16-41-26.zip --out /tmp/test 
python buganalysis.py -v --eventbypid --file bugreport-tphoneY-T5711INDURG-264-2018-07-30-16-41-26.zip --out /tmp/test --tester Mr.ABC --dev Mr.XYZ --bugid 45882 --bugtitle "Phone app crashed"
