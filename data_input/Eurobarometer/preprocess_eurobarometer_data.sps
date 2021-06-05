* Encoding: UTF-8.
* Made by Rianne Schouten on 28-05-2021
* Encoding: UTF-8.

dataset close all.
get /file = 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Eurobarometer\ZA3521_v2-0-1.sav'.

SET WORKSPACE 1311632.

FILTER OFF.
USE ALL.
SELECT IF (eb  > 3).
EXECUTE.

* unification of eu
*RECODE unifictn (3=0) (4=0) (Lowest thru 2=1) (ELSE=SYSMIS) INTO Uni_bin.
*VARIABLE LABELS  Uni_bin 'Uni_bin'.
*EXECUTE.
*MEANS TABLES=Uni_bin BY eb
 * /CELLS=MEAN COUNT STDDEV SEMEAN MEDIAN.

*left-right wing oriented

RECODE lrs (Lowest thru 10=Copy) (ELSE=SYSMIS) INTO lrsnum.
VARIABLE LABELS  lrsnum 'lrsnum'.
EXECUTE.
variable level  lrsnum (scale).
EXAMINE VARIABLES=lrsnum BY eb
  /PLOT BOXPLOT
  /COMPARE GROUPS
  /PERCENTILES(5,10,25,50,75,90,95)
  /STATISTICS DESCRIPTIVES
  /CINTERVAL 95
  /MISSING LISTWISE
  /NOTOTAL.

* speed

RECODE euspeed1 (Lowest thru 7=Copy) (ELSE=SYSMIS) INTO euspeed1num.
VARIABLE LABELS  euspeed1num 'euspeed1num'.
EXECUTE.
variable level  euspeed1num (scale).
EXAMINE VARIABLES=euspeed1num BY eb
  /PLOT BOXPLOT
  /COMPARE GROUPS
  /PERCENTILES(5,10,25,50,75,90,95)
  /STATISTICS DESCRIPTIVES
  /CINTERVAL 95
  /MISSING LISTWISE
  /NOTOTAL.

* here manual recoding of values 
* specification of type of variable
* complete are: id, year, eb, nation1
* sex

RECODE sex (8=SYSMIS) (9=SYSMIS).
EXECUTE.
FREQUENCIES VARIABLES=sex
  /ORDER=ANALYSIS.

* age

RECODE age (0=SYSMIS).
EXECUTE.

DELETE VARIABLES study_id version nation2 eleclist wsample wnation 
    weuro euspeed2 speedup feelclo voteint inclvote lastvote euvonext unions
    agerec1 agerec2 agerec3 agerec4 occup lstoccup secoccup firm1 firm2
   occuphh lstocchh soclass denom income sizecmty regionat language matpmat eppi.

RECODE unifictn membrshp benefit regret comm commf ecpres 
    ecpresf epinfo epinfof epimp1 epimp2 epimpf epelfut mepatt eurogov semmedia semhope semgood trustep 
    trustec trustcm trustcj trusteo trustecb trusteca trustcr trustsec ecfinfo ecint3 ecint4 ecimp 
    underst feel citizen cpcultur cpcurr cpdatap cpdrugs cpeduc cpenvir cpforpol cpimmigr cpindust 
    cppasyl cppress cpscien cpsecur cpthird cpunemp cpvatax cpwelfar cpworker cpworsec satislfe 
    happinss better econpast finapast peaceful conflict conflict worldwar poldisc persuade polint newstv newspap 
    newsrad sochange valpri1 valpri2 relimp natpride satisdmo satisdeu efficacy mvanm mvanw mvecol 
    mvnatur closepty particip party unionr unionhh educrec hh mhw mie typecmty churchat religf1 religf2 
    oli scmi tea euspeed1 (8 = SYSMIS) (9=SYSMIS).
EXECUTE.

RECODE worldwar lrs married educ sizehh children 
    childold childyng (96 = SYSMIS) (97 = SYSMIS) (98 = SYSMIS) (99=SYSMIS).
EXECUTE.

RECODE mediause (7 = SYSMIS) (8 = SYSMIS) (9 = SYSMIS). 
    EXECUTE.

save 
/outfile= 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Eurobarometer\ZA3521_v2-0-1_recoded.sav'
/keep = all.

* this filter is for euspeed1
    
dataset close all.
get /file = 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Eurobarometer\ZA3521_v2-0-1_recoded.sav'.

SET WORKSPACE 1311632.

CROSSTABS
  /TABLES=eb BY euspeed1num
  /FORMAT=AVALUE TABLES
  /CELLS=COUNT
  /COUNT ROUND CELL.

USE ALL.
COMPUTE filter_$=((eb ~= 400) and (eb ~= 410) and (eb ~= 541) and (eb ~= 562) and (eb ~= 420) and (eb ~= 441) and ~(SYSMIS(euspeed1num))).
VALUE LABELS filter_$ 0 'Not Selected' 1 'Selected'.
FORMATS filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE.

FILTER OFF.
USE ALL.
SELECT IF (filter_$ = 1).
EXECUTE.

DELETE VARIABLES filter_$.

CROSSTABS
  /TABLES=eb BY euspeed1num
  /FORMAT=AVALUE TABLES
  /CELLS=COUNT
  /COUNT ROUND CELL.

FREQUENCIES VARIABLES=eb
  /ORDER=ANALYSIS.

save 
/outfile= 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Eurobarometer\ZA3521_v2-0-1_euspeed1num.sav'
/keep = all.

* this filter is for lrsnum
    
dataset close all.
get /file = 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Eurobarometer\ZA3521_v2-0-1_recoded.sav'.

SET WORKSPACE 1311632.

CROSSTABS
  /TABLES=eb BY lrsnum
  /FORMAT=AVALUE TABLES
  /CELLS=COUNT
  /COUNT ROUND CELL.

USE ALL.
COMPUTE filter_$=((eb ~= 101) and (eb ~= 311) and (eb ~= 321) and (eb ~= 341) and (eb ~= 351) and 
    (eb ~= 371) and (eb ~= 381) and (eb ~= 391) and (eb ~= 411) and (eb ~= 431) and (eb ~= 432) and
    (eb ~= 441) and (eb ~= 461) and (eb ~= 470) and (eb ~= 472) and (eb ~= 501) and (eb ~= 521) and
     (eb ~= 551) and  (eb ~= 552) and  (eb ~= 560) and (eb ~= 562) and (eb ~= 563) and (eb ~= 570) and
      (eb ~= 572) and ~(SYSMIS(lrsnum))).
VALUE LABELS filter_$ 0 'Not Selected' 1 'Selected'.
FORMATS filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE.

FILTER OFF.
USE ALL.
SELECT IF (filter_$ = 1).
EXECUTE.

DELETE VARIABLES filter_$.

CROSSTABS
  /TABLES=eb BY lrsnum
  /FORMAT=AVALUE TABLES
  /CELLS=COUNT
  /COUNT ROUND CELL.

FREQUENCIES VARIABLES=eb
  /ORDER=ANALYSIS.

save 
/outfile= 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Eurobarometer\ZA3521_v2-0-1_lrsnum.sav'
/keep = all.























