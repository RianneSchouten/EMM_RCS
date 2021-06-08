* Encoding: UTF-8.
*Made by Rianne Schouten, 04-06-2021

dataset close all.
get /file = 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Brexit\BrexitAttitudes_Data.sav'.

RECODE BrexitID (1=1) (2 thru 4=0) (ELSE=Copy) INTO Leaver.
VARIABLE LABELS  Leaver 'Leaver'.
EXECUTE.

RECODE BrexitID (2=1) (3 thru 4=0) (1=0) (ELSE=Copy) INTO Remainer.
VARIABLE LABELS  Remainer 'Remainer'.
EXECUTE.

DELETE VARIABLES Remainimport Leaverimport BrexitID endtime starttime ethnicity1 ethnicity2 
    profile_gross_household socialgradeCIE1 Weight GEvote2015 GEvote2017 GEvote2019 
    education_level newspaper_readership partyid political_attention ID.
       
recode region work_stat work_organisation work_type (98 = SYSMIS) (99 = SYSMIS). 
    execute.

recode EURef2016 (99 = SYSMIS).
    execute.

recode work_organisation Hindsight Poscountry Govthand Genecon Posind (8 = SYSMIS) (9 = SYSMIS).
    execute.

recode profile_gross_personal (15 = SYSMIS) (16 = SYSMIS) (98 = SYSMIS) (99 = SYSMIS).
    execute.

recode education_age (7 = SYSMIS) (8 = sysmis) (9 = SYSMIS).
 EXECUTE.

RECODE socialgradeCIE2  (7 = SYSMIS) (8 = sysmis)  (98 = SYSMIS) (99 = SYSMIS).
EXECUTE.

RECODE Tradeimmig (998 = SYSMIS) (999 = SYSMIS).
EXECUTE.

RECODE age (98 = 6) (32766 = SYSMIS). 
execute.

FREQUENCIES VARIABLES=sex region EURef2016 profile_gross_personal 
    education_age socialgradeCIE2 work_stat work_organisation work_type Hindsight Poscountry Posind 
    Govthand Tradeimmig Genecon Leaver Remainer
  /ORDER=ANALYSIS.

save 
/outfile= 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Brexit\Brexit_preprocessed.sav'
/keep = all.

* we delete more variables that have a high correlation with leaver
    
dataset close all.

get /file = 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Brexit\Brexit_preprocessed.sav'.
    
CORRELATIONS
  /VARIABLES=age sex region EURef2016 profile_gross_personal education_age socialgradeCIE2 
    work_stat work_organisation work_type Hindsight Poscountry Posind Govthand Tradeimmig Genecon 
    Leaver Remainer
  /PRINT=TWOTAIL NOSIG FULL
  /MISSING=PAIRWISE.
    
DELETE VARIABLES Hindsight Poscountry Posind.
   
save 
/outfile= 'C:\Users\20200059\Documents\Github\EMM_RCS\data_input\Brexit\Brexit_preprocessed_without.sav'
/keep = all.
