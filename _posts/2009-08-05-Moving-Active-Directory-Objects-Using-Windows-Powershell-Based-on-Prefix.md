---           
layout: post
title: Moving Active Directory Objects Using Windows Powershell Based on Prefix
date: 2009-08-05 21:58:32 UTC
updated: 2009-08-05 21:58:32 UTC
comments: false
categories: 
---
So todays goal was to use the Quest ActiveRoles AD Management CMDLets to examine objects in the Active Directory and then move them into an OU Based on the Prefix in their name. For example computers starting with MLW go to the MLW OU nested under a SearchRoot in our case lab Workstations. I couldn't find any examples of this so I decided to post the code here in case any one else is having the same problem. Now onto Powershell Signing Best Practices.   

\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  
\# MoveComputers.ps1   
\# v1.0  
\#   
\# Author: Daniel DeFreez  
\# Author: Andrew Krug  
\#   
\# This script is designed to be run as a scheduled task.  
\# It looks through the LabWorksations OU (SOUComputers/SOUWorkstations/AshlandWorkstations/LabWorkstations)  
\# for computers with name prefixes matching an OU below LabWorkstations and moves the computer objects to that OU.   
\# For example, LABLANG-01564 would be moved into the 'LANG' OU below LabWorkstations. A computer will not be moved   
\# if has already been placed in a container below the root of LabWorkstations.  
\#   
\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  

Add-PSSNapin Quest.ActiveRoles.ADManagement -errorAction silentlyContinue  

\# Location of the LabWorkstations OU  
$labWorkstations = 'home.ad.sou.edu/SOUComputers/SOUWorkstations/AshlandWorkstations/LabWorkstations'  

$oUnits = Get-QADObject -SearchRoot $labWorkstations -Type OrganizationalUnit  
$computers = Get-QADComputer -SearchRoot $labWorkstations -SearchScope onelevel   

if (!$computers) { exit }  

foreach ($c in $computers) {  
\# Strip off 'LAB' from Computer Name and grab only the part before the '-'  
$prefix = $c.Name.SubString(3, $c.Name.Length - 3).split("-")\[0\]   
$newOU = $oUnits | Where-Object { $\_.Name -eq $prefix }   

\# Move the Computer if the OU matches the prefix (isn't null)  
if ($newOU) {   
Move-QADObject $c -NewParentContainer $newOU \> $null  
}  
}

www.andrewkrug.com E-Mail Comments to andrewkrug@gmail.com