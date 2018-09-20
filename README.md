The bugreport analysis tool to sort bug report data

cd bugreport_analysis_tool

Usage:<br>
buganalysis.py <options>  --file  bugreport.zip --out /tmp/test <br>

options:<br>
	-h,--help		- print help <br>
	-v,--verbose		- print verbose logging <br>
	--file <filename>	- zip or txt file of bugreport<br>
	--out <out_dir>		- output dir<br>
	--bugid <bug number>	- Redmine bug number<br>
	--bugtitle <bug title>	- Redmine bug title<br>
	--dev <developer name>	- Developer name<br>
	--tester <tester name>	- Test engineer name<br>
	--eventbypid		- Filter event logs by pid<br>
	--version		- print version<br>



Examples:<br>
python buganalysis.py -v --file bugreport-tphoneY-T5711INDURG-264-2018-07-30-16-41-26.zip --out /tmp/test <br><br>
python buganalysis.py -v --eventbypid --file bugreport-tphoneY-T5711INDURG-264-2018-07-30-16-41-26.zip --out /tmp/test --tester Mr.ABC --dev Mr.XYZ --bugid 45882 --bugtitle "Phone app crashed"<br>
