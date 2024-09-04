#-------------------------------------------------------------------------------
# Name:        ejscreenbatch
# Purpose:     calculate EJSCREEN indexes.
#
# Author:      SAIC, EPA OEI Contractor
#
# Created:     11/11/2014
# Updated:     09/4/2024
# Copyright:
# Licence:
#-------------------------------------------------------------------------------

import http.client, urllib.request, urllib.parse, urllib.error, json
import arcpy
import os
import sys
import math
import ejconfig


from arcpy import env

templyr = "ej_lyr"
templyr_st = "ej_lyr_st"
def main(fc,distance,unit,ejws,outFC):
    popfileds ={"ACSTOTPOP":"total population (ACS2022)",\
    "ACSIPOVBAS":"Total Population for whom Poverty Status is Determined",\
    "ACSEDUCBAS":"Total Population Age 25 up",\
    "ACSTOTHH":"Total Households",\
    "PRE1960":"Houses Built Pre 1960",\
    "ACSUNEMPBAS": "Persons in civilian labor force",\
    "ACSDISABBAS": "Civilian non-institutionalized population"\
    }
    arcpy.env.overwriteOutput = True
    desc = arcpy.Describe(fc)
    fcsr = desc.spatialReference
    if fcsr.type == "Unknown":
        sr = arcpy.SpatialReference(4326)
        arcpy.DefineProjection_management(fc,sr)
    outfile = os.path.basename(outFC)
    firstletter = outfile[0]
    if firstletter.isdigit():
        arcpy.AddWarning("output feature class name cannot start with number. '" + outfile + "' is invalid file name")
        sys.exit()
    arcpy.AddMessage("Output feature: " + outFC)
    env.workspace = os.path.dirname(outFC)
    arcpy.CopyFeatures_management(fc, outfile)
    fieldsobj = constructHASH()
    fieldList = []
    for pf in popfileds:
        pdesc = popfileds[pf]
        mod_pf = "_" + pf
        pfld =[mod_pf,'LONG', pdesc]
        fieldList.append(pfld)
    buffld = ['_buff','TEXT','Buffer distance']
    fieldList.append(buffld)
    stfld = ['_stabbr','TEXT','State Abbreviation']
    fieldList.append(stfld)
    stnamefld = ['_statename','TEXT','State Name']
    fieldList.append(stnamefld)
    regfld = ['_region','TEXT','EPA region number']
    #fieldList.append(regfld)
    for key in fieldsobj:
        
      pdfname = ejdataobj[key]["pdfname"]
      basedesc = ejdataobj[key]["desc"]
      indexcode = ejdataobj[key]["contenttype"]
      if indexcode == "P_EJ2":
          stpdffld = "S_P2_" + pdfname
          #regpdffld = "R_P_" + pdfname
          natpdffld = "N_P2_" + pdfname
          stpdffld_desc = "State percentile for " + basedesc
          #regpdffld_desc = "Regional percentile for " + basedesc
          natpdffld_desc = "National percentile for " + basedesc
          fieldList.append(["_" + stpdffld,'TEXT',stpdffld_desc])
          #fieldList.append(["_" + regpdffld,'TEXT',regpdffld_desc])
          fieldList.append(["_" + natpdffld,'TEXT',natpdffld_desc])
        
      if indexcode == "P_EJ5":
          stpdffld = "S_P5_" + pdfname
          #regpdffld = "R_P_" + pdfname
          natpdffld = "N_P5_" + pdfname
          stpdffld_desc = "State percentile for " + basedesc
          #regpdffld_desc = "Regional percentile for " + basedesc
          natpdffld_desc = "National percentile for " + basedesc
          fieldList.append(["_" + stpdffld,'TEXT',stpdffld_desc])
          #fieldList.append(["_" + regpdffld,'TEXT',regpdffld_desc])
          fieldList.append(["_" + natpdffld,'TEXT',natpdffld_desc])

      elif indexcode == "P_ENV":
          rawpdffld = "RAW_E_" + pdfname
          stpctfld = "S_E_" + pdfname + "_PER"
          #regpctfld = "R_E_" + pdfname + "_PER"
          natpctfld = "N_E_" + pdfname + "_PER"
          stavgfld = "S_E_" + pdfname
          #regavgfld = "R_E_" + pdfname
          natavgfld = "N_E_" + pdfname
          rawpdffld_desc = "Raw data for " + basedesc
          stpctfld_desc = "State percentile for " + basedesc
          #regpctfld_desc = "Regional percentile for " + basedesc
          natpctfld_desc = "National percentile for " + basedesc
          stavgfld_desc = "State average for " + basedesc
          #regavgfld_desc = "Regional average for " + basedesc
          natavgfld_desc = "National average for " + basedesc
          fieldList.append(["_" + rawpdffld,'TEXT',rawpdffld_desc])
          fieldList.append(["_" + stpctfld,'TEXT',stpctfld_desc])
          #fieldList.append(["_" + regpctfld,'TEXT',regpctfld_desc])
          fieldList.append(["_" + natpctfld,'TEXT',natpctfld_desc])
          fieldList.append(["_" + stavgfld,'TEXT',stavgfld_desc])
          #fieldList.append(["_" + regavgfld,'TEXT',regavgfld_desc])
          fieldList.append(["_" + natavgfld,'TEXT',natavgfld_desc])

      elif indexcode == "P_DEM":
          rawpdffld = "RAW_D_" + pdfname
          stpctfld = "S_D_" + pdfname + "_PER"
#          regpctfld = "R_D_" + pdfname + "_PER"
          natpctfld = "N_D_" + pdfname + "_PER"
          stavgfld = "S_D_" + pdfname
#          regavgfld = "R_D_" + pdfname
          natavgfld = "N_D_" + pdfname
          rawpdffld_desc = "Raw data for " + basedesc
          stpctfld_desc = "State percentile for " + basedesc
#          regpctfld_desc = "Regional percentile for " + basedesc
          natpctfld_desc = "National percentile for " + basedesc
          stavgfld_desc = "State average for " + basedesc
#          regavgfld_desc = "Regional average for " + basedesc
          natavgfld_desc = "National average for " + basedesc
          fieldList.append(["_" + rawpdffld,'TEXT',rawpdffld_desc])
          fieldList.append(["_" + stpctfld,'TEXT',stpctfld_desc])
#          fieldList.append(["_" + regpctfld,'TEXT',regpctfld_desc])
          fieldList.append(["_" + natpctfld,'TEXT',natpctfld_desc])
          fieldList.append(["_" + stavgfld,'TEXT',stavgfld_desc])
#          fieldList.append(["_" + regavgfld,'TEXT',regavgfld_desc])
          fieldList.append(["_" + natavgfld,'TEXT',natavgfld_desc])

    arcpy.AddFields_management(outFC,  fieldList)
    rows = arcpy.UpdateCursor(outFC)
    arcpy.env.workspace = ejws
    if arcpy.Exists("EJSCREEN_Primary"):
        inejscreen = ejws + "\EJScreen_Primary"
    elif arcpy.Exists("EJSCREEN_Full_with_AS_CNMI_GU_VI"):
        inejscreen = ejws + "\EJSCREEN_Full_with_AS_CNMI_GU_VI"

    inejcreen_st = ejws + "\EJSCREEN_StatePct_with_AS_CNMI_GU_VI"

    arcpy.MakeFeatureLayer_management(inejscreen, templyr)
    arcpy.MakeFeatureLayer_management(inejcreen_st, templyr_st)
    lstFields = arcpy.ListFields(templyr)
    del ejdataobj["DEMOGIDX_2ST"]
    del ejdataobj["DEMOGIDX_5ST"]
  
    with arcpy.da.SearchCursor(fc, ["SHAPE@", "SHAPE@X", "SHAPE@Y"]) as cursor:
        feaCount = 1
        for rec in cursor:
            geom = rec[0]
            geomx = rec[1]
            geomy = rec[2]
            if geom is None:
                arcpy.AddMessage("Feature #" + str(feaCount) + ": no geometry defined. Skip this record.")
                feaCount += 1
#                assignNA_2(rows,geom,"","","")
                assignNA_2(rows,geom,"","")
                continue
            
            if geomx == 0 or geomy == 0:
                arcpy.AddMessage("Feature #" + str(feaCount) + ": has an X and/or Y value of 0. Skip this record.")
                feaCount += 1
#                assignNA_2(rows,geom,"","","")
                assignNA_2(rows,geom,"","")
                continue

            idist = 0
            if len(distance) > 0:
                idist = float(distance)

            if idist > 0:
                temPol = arcpy.Geometry()
                buff = distance + " " + unit
                poly = arcpy.Buffer_analysis([geom], temPol, buff,method='GEODESIC')[0]
                bgweightobj = calBGweight(poly)
             

#                stabbr,stname,regnum = getStateRegion(geom)
                stabbr,stname = getStateRegion(geom)
##                arcpy.AddMessage(stabbr + ": " + stname + "; "+ regnum)
                if type(bgweightobj) == type(None):
                    arcpy.AddMessage("No blockgroup record found in the study area")
                    #assignNA(rows,geom,stname,stabbr,regnum)
#                    assignNA_2(rows,geom,stabbr,stname,regnum)
                    assignNA_2(rows,geom,stabbr,stname)
                else:
                    arcpy.SelectLayerByLocation_management(templyr,"INTERSECT",poly,'',"NEW_SELECTION")
                    arcpy.SelectLayerByLocation_management(templyr_st,"INTERSECT",poly,'',"NEW_SELECTION")
                    result = arcpy.GetCount_management(templyr)
                    
               
                    fcount = int(result.getOutput(0))
                    arcpy.AddMessage("Feature #" + str(feaCount) + ": " + str(fcount) + " BGs")
                    feaCount += 1
                    if fcount > 0:
                        with arcpy.da.SearchCursor(templyr, ["ACSTOTPOP", "ACSIPOVBAS", "ACSEDUCBAS", 'ACSTOTHH', 'ACSTOTHU', 'ID']) as cursor: 
                            nullflag = False
                            for bg in cursor:
                                
                                if bg[0] == None or bg[1] == None or bg[2] == None or bg[3] == None or bg[4] == None:
                                    arcpy.AddMessage("Block group ID " + bg[5] + " has a null value in a population field. Skip this record")
                                    nullflag = True
                        if nullflag == True:
                            assignNA_2(rows,geom,"","","")
                            continue
                  
#                        arr = arcpy.da.FeatureClassToNumPyArray(templyr,'*', null_value=math.nan) 
                        arr = arcpy.da.FeatureClassToNumPyArray(templyr, ["ID","STATE_NAME","ST_ABBREV","CNTY_NAME","REGION",
"ACSTOTPOP","ACSIPOVBAS","ACSEDUCBAS","ACSTOTHH","ACSTOTHU","ACSUNEMPBAS", "ACSDISABBAS", 
"PEOPCOLOR","LOWINCOME", "UNEMPLOYED", "DISABILITY", "LINGISO","LESSHS","UNDER5","OVER64","PRE1960",
"DEMOGIDX_2","DEMOGIDX_5", "PEOPCOLORPCT","LOWINCPCT","UNEMPPCT","DISABILITYPCT","LINGISOPCT","LESSHSPCT","UNDER5PCT","OVER64PCT","LIFEEXPPCT",
"PM25","OZONE","DSLPM","RSEI_AIR","PTRAF","PRE1960PCT","PNPL","PRMP","PTSDF","UST","PWDIS", "DWATER", "NO2", 
"D2_PM25","D2_OZONE","D2_DSLPM","D2_RSEI_AIR","D2_PTRAF","D2_LDPNT","D2_PNPL","D2_PRMP","D2_PTSDF","D2_UST","D2_PWDIS", "D2_DWATER", "D2_NO2",
"D5_PM25","D5_OZONE","D5_DSLPM","D5_RSEI_AIR","D5_PTRAF","D5_LDPNT","D5_PNPL","D5_PRMP","D5_PTSDF","D5_UST","D5_PWDIS","D5_DWATER", "D5_NO2"]) 

                        arr_st = arcpy.da.FeatureClassToNumPyArray(templyr_st, ["ID","STATE_NAME","ST_ABBREV","CNTY_NAME","REGION",
"ACSTOTPOP","ACSIPOVBAS","ACSEDUCBAS","ACSTOTHH","ACSTOTHU","ACSUNEMPBAS", "ACSDISABBAS", 
"PEOPCOLOR","LOWINCOME", "UNEMPLOYED", "DISABILITY", "LINGISO","LESSHS","UNDER5","OVER64","PRE1960",
"DEMOGIDX_2","DEMOGIDX_5","PEOPCOLORPCT","LOWINCPCT","UNEMPPCT","DISABILITYPCT","LINGISOPCT","LESSHSPCT","UNDER5PCT","OVER64PCT","LIFEEXPPCT",
"PM25","OZONE","DSLPM","RSEI_AIR","PTRAF","PRE1960PCT","PNPL","PRMP","PTSDF","UST","PWDIS", "DWATER", "NO2", 
"D2_PM25","D2_OZONE","D2_DSLPM","D2_RSEI_AIR","D2_PTRAF","D2_LDPNT","D2_PNPL","D2_PRMP","D2_PTSDF","D2_UST","D2_PWDIS", "D2_DWATER", "D2_NO2",
"D5_PM25","D5_OZONE","D5_DSLPM","D5_RSEI_AIR","D5_PTRAF","D5_LDPNT","D5_PNPL","D5_PRMP","D5_PTSDF","D5_UST","D5_PWDIS","D5_DWATER", "D5_NO2"]) 
                        popList = {}
                        
                        for pf in popfileds:
                            
                            tpop =calPop(arr, bgweightobj,pf)
                            popList[pf] = tpop
                        for fld in ejdataobj:
                          
                           
                            if checkfield(fld,lstFields):
                                pmvalue = weight_Avg(arr, fld,bgweightobj)
                                pmvalue_st = weight_Avg(arr_st, fld,bgweightobj)
                                ejdataobj[fld]["raw_value"] = pmvalue
                                ejdataobj[fld]["raw_value_st"] = pmvalue_st
                                ejdataobj[fld]["hasvalue"] = True
                            else:
                                pmvalue = "N/A"
                                ejdataobj[fld]["raw_value"] = pmvalue
                                ejdataobj[fld]["raw_value_st"] = pmvalue
                                ejdataobj[fld]["hasvalue"] = False
                        if len(stabbr) > 0:
                            if stabbr == "PR":
#                                calPercentile_PR(stabbr,regnum)
                                calPercentile_PR(stabbr)
                            else:
#                                calPercentile(stabbr,regnum)
                                calPercentile(stabbr)
#                            populateFields_2(rows,geom,stabbr,stname,regnum,popList)
                            populateFields_2(rows,geom,stabbr,stname,popList)
                        else:
#                            assignNA_2(rows,geom,stabbr,stname,regnum)
                            assignNA_2(rows,geom,stabbr,stname)
                    else:
                        #assignNA(rows,geom,stabbr,stname,regnum)
#                        assignNA_2(rows,geom,stabbr,stname,regnum)
                        assignNA_2(rows,geom,stabbr,stname)
    arcpy.AddMessage("Processed completed.")
    arcpy.AddMessage("A 'null' value in the results indicates that a buffered area is sparsely populated or no data is available for the buffered area.")

def checkfield(infld,fieldlist):

    x = False
    for field in fieldlist:
        if field.name == infld:
            x = True
    return x

#def populateFields_2(rows,pnt,stabbr,stname,regnum,pList):
def populateFields_2(rows,pnt,stabbr,stname,pList):
    
    row = next(rows)
    buffstr = dx + " " + ux
    for popfld in pList:
        pvalue = pList[popfld]
        
        row.setValue("_" + popfld,pvalue)
    row.setValue('_buff',buffstr)
    row.setValue('_stabbr',stabbr)
    row.setValue('_statename',stname)
#    row.setValue('_region',regnum)
    for fld in ejdataobj:
       
        ctype = ejdataobj[fld]["contenttype"]
        pdfname =ejdataobj[fld]["pdfname"]
        if ctype == "P_EJ2":
            stpdffld = "S_P2_" + pdfname
#            regpdffld = "R_P_" + pdfname
            natpdffld = "N_P2_" + pdfname

            v_stpdfld = ejdataobj[fld]["statepctile"]
            row.setValue("_" + stpdffld,v_stpdfld)

#            v_regpdffld = ejdataobj[fld]["regionpctile"]
#            row.setValue("_" + regpdffld,v_regpdffld)

            v_natpdffld = ejdataobj[fld]["nationpctile"]
            row.setValue("_" + natpdffld,v_natpdffld)


        if ctype == "P_EJ5":
            stpdffld = "S_P5_" + pdfname
#            regpdffld = "R_P_" + pdfname
            natpdffld = "N_P5_" + pdfname


            v_stpdfld = ejdataobj[fld]["statepctile"]
            row.setValue("_" + stpdffld,v_stpdfld)

#            v_regpdffld = ejdataobj[fld]["regionpctile"]
#            row.setValue("_" + regpdffld,v_regpdffld)

            v_natpdffld = ejdataobj[fld]["nationpctile"]
            row.setValue("_" + natpdffld,v_natpdffld)

        elif ctype == "P_ENV":
            rawpdffld = "RAW_E_" + pdfname
            stpctfld = "S_E_" + pdfname + "_PER"
#            regpctfld = "R_E_" + pdfname + "_PER"
            natpctfld = "N_E_" + pdfname + "_PER"
            stavgfld = "S_E_" + pdfname
#            regavgfld = "R_E_" + pdfname
            natavgfld = "N_E_" + pdfname
            v_rawpdffld = ejdataobj[fld]["raw_value"]
            fmt =ejdataobj[fld]["formatter"]
            natastatus =ejdataobj[fld]["isnata"]
            if fmt.isdigit():
                v_rawpdffld = getEnvText(ejdataobj[fld]["raw_value"],fmt)

            row.setValue("_" + rawpdffld,v_rawpdffld)
            v_stpdfld = ejdataobj[fld]["statepctile"]
            row.setValue("_" + stpctfld,v_stpdfld)
#            v_regpdffld = ejdataobj[fld]["regionpctile"]
#            if natastatus == "Y":
#                v_regpdffld = getNATApctText(v_regpdffld)
#            row.setValue("_" + regpctfld,v_regpdffld)

            v_natpdffld = ejdataobj[fld]["nationpctile"]
            if natastatus == "Y":
                v_natpdffld = getNATApctText(v_natpdffld)
            row.setValue("_" + natpctfld,v_natpdffld)

            v_stavgfld = ejdataobj[fld]["stateavg"]
            if fmt.isdigit():
                v_stavgfld = getEnvText(v_stavgfld,fmt)
            row.setValue("_" + stavgfld,v_stavgfld)
#            v_regavgfld = ejdataobj[fld]["regionavg"]
#            if fmt.isdigit():
#                v_regavgfld = getEnvText(v_regavgfld,fmt)
#            row.setValue("_" + regavgfld,v_regavgfld)
            v_natavgfld = ejdataobj[fld]["nationavg"]
            if fmt.isdigit():
                v_natavgfld = getEnvText(v_natavgfld,fmt)
            row.setValue("_" + natavgfld,v_natavgfld)
        elif ctype == "P_DEM":
            rawpdffld = "RAW_D_" + pdfname
            stpctfld = "S_D_" + pdfname + "_PER"
#            regpctfld = "R_D_" + pdfname + "_PER"
            natpctfld = "N_D_" + pdfname + "_PER"
            stavgfld = "S_D_" + pdfname
#            regavgfld = "R_D_" + pdfname
            natavgfld = "N_D_" + pdfname
            v_rawpdffld = ejdataobj[fld]["raw_value"]
            fmt =ejdataobj[fld]["formatter"]
            v_rawpdffld = ejdataobj[fld]["raw_value"]
##            arcpy.AddMessage("raw value: " + str(v_rawpdffld))
            if fmt == "%" and v_rawpdffld != 'N/A':
                v_rawpdffld = str(roundNumber(float(v_rawpdffld) * 100, 0)) + '%'
            
            if fmt.isdigit() and v_rawpdffld != 'N/A':
                v_rawpdffld = str(round(v_rawpdffld, int(fmt)))
            row.setValue("_" + rawpdffld,v_rawpdffld)
            v_stpdfld = ejdataobj[fld]["statepctile"]
            row.setValue("_" + stpctfld,v_stpdfld)
#            v_regpdffld = ejdataobj[fld]["regionpctile"]
#            row.setValue("_" + regpctfld,v_regpdffld)
            v_natpdffld = ejdataobj[fld]["nationpctile"]
            row.setValue("_" + natpctfld,v_natpdffld)
            v_stavgfld = ejdataobj[fld]["stateavg"]
            if fmt == "%" and v_stavgfld != 'N/A':
                    v_stavgfld = str(roundNumber(float(v_stavgfld) * 100, 0)) + '%'

            if fmt.isdigit() and v_stavgfld != 'N/A':
                v_stavgfld = str(round(v_stavgfld, int(fmt)))
            row.setValue("_" + stavgfld,v_stavgfld)
#            v_regavgfld = ejdataobj[fld]["regionavg"]
#            if fmt == "%" and v_regavgfld != 'N/A':
#                v_regavgfld = str(roundNumber(float(v_regavgfld) * 100, 0)) + '%'
#            row.setValue("_" + regavgfld,v_regavgfld)
            v_natavgfld = ejdataobj[fld]["nationavg"]
            if fmt == "%" and v_natavgfld != 'N/A':
                v_natavgfld = str(roundNumber(float(v_natavgfld) * 100, 0)) + '%'

            if fmt.isdigit() and v_natavgfld != 'N/A':
                v_natavgfld = str(round(v_natavgfld, int(fmt)))
            row.setValue("_" + natavgfld,v_natavgfld)
    rows.updateRow(row)


#def assignNA_2(rows,pnt,stabbr,stname,regnum):
def assignNA_2(rows,pnt,stabbr,stname):

    row = next(rows)
    buffstr = dx + " " + ux
    row.setValue('_buff',buffstr)
    row.setValue('_stabbr',stabbr)
    row.setValue('_statename',stname)
#    row.setValue('_region',regnum)
    if len(stabbr) > 0:
#        calAvgValue(stabbr,regnum)
        calAvgValue(stabbr)
        for fld in ejdataobj:
            ctype = ejdataobj[fld]["contenttype"]
            pdfname =ejdataobj[fld]["pdfname"]
            fmt =ejdataobj[fld]["formatter"]
            if ctype == "P_ENV":
                stavgfld = "S_E_" + pdfname
#                regavgfld = "R_E_" + pdfname
                natavgfld = "N_E_" + pdfname
                v_stavgfld = ejdataobj[fld]["stateavg"]
                if fmt.isdigit():
                    v_stavgfld = getEnvText(v_stavgfld,fmt)
                row.setValue("_" + stavgfld,v_stavgfld)
#                v_regavgfld = ejdataobj[fld]["regionavg"]
#                if fmt.isdigit():
#                    v_regavgfld = getEnvText(v_regavgfld,fmt)
#                row.setValue("_" + regavgfld,v_regavgfld)
                v_natavgfld = ejdataobj[fld]["nationavg"]
                if fmt.isdigit():
                    v_natavgfld = getEnvText(v_natavgfld,fmt)
                row.setValue("_" + natavgfld,v_natavgfld)
            elif ctype == "P_DEM":
                stavgfld = "S_D_" + pdfname
#                regavgfld = "R_D_" + pdfname
                natavgfld = "N_D_" + pdfname
                v_stavgfld = ejdataobj[fld]["stateavg"]
                if fmt == "%" and v_stavgfld != 'N/A':
                    v_stavgfld = str(roundNumber(float(v_stavgfld) * 100, 0)) + '%'
                row.setValue("_" + stavgfld,v_stavgfld)
#                v_regavgfld = ejdataobj[fld]["regionavg"]
#                if fmt == "%" and v_regavgfld != 'N/A':
#                    v_regavgfld = str(roundNumber(float(v_regavgfld) * 100, 0)) + '%'
#                row.setValue("_" + regavgfld,v_regavgfld)
                v_natavgfld = ejdataobj[fld]["nationavg"]
                if fmt == "%" and v_natavgfld != 'N/A':
                    v_natavgfld = str(roundNumber(float(v_natavgfld) * 100, 0)) + '%'
                row.setValue("_" + natavgfld,v_natavgfld)
    rows.updateRow(row)

def weight_Avg(fsetw, att,bgweightobj):
  
    bgIDfieldname = "ID"
    popfieldname = ejdataobj[att]["denominator"]
    if popfieldname is None:
        popfieldname = "ACSTOTPOP"
    vsum = 0
    popsum = 0
    noData = True
    noRaw = True
    for r in fsetw:
        bgnum = str(r[bgIDfieldname])
        fieldvalue = r[att]

##        print bgnum
        if bgnum in bgweightobj:
            noData = False
            bgwt = bgweightobj[bgnum]
            if type(bgwt) == type(None) or (not bgwt):
                bgwt = 0
            popvalue =r[popfieldname]

            if type(popvalue) == type(None) or (not popvalue):
                popvalue = 0.0
            else:
                popvalue = float(popvalue)

            bgpop = bgwt * popvalue
            popsum = popsum + bgpop
            ##print "bgnum: " + bgnum + "; popsum: " + str(popsum) + "; fieldvalue: " + str(fieldvalue)
            if math.isnan(fieldvalue):
                fieldvalue = 0
            else:
                noRaw = False

            vsum = vsum + fieldvalue * bgpop

    if noData or noRaw:
        return 'N/A'
    elif popsum > 0:
        finalvalue = vsum / popsum
        if math.isnan(finalvalue):
            return 'N/A'
        else:
            return finalvalue
    else:
        return 'N/A'

def calPop(fsetw, bgweightobj,popfieldname):
   
    bgIDfieldname = "ID"

    popsum = 0
    for r in fsetw:
        bgnum = str(r[bgIDfieldname])
        #arcpy.AddMessage(popfieldname + ": " + bgnum)
        if bgnum in bgweightobj:
            bgwt = bgweightobj[bgnum]
            if type(bgwt) == type(None) or (not bgwt):
                bgwt = 0
            popvalue =r[popfieldname]

            if type(popvalue) == type(None) or (not popvalue):
                popvalue = 0.0
            else:
                popvalue = float(popvalue)

            bgpop = bgwt * popvalue
            popsum = popsum + bgpop
    return round(popsum,0)

def getStateRegion(geom):
    
    ##diststr = dx + " " + ux
    diststr = "1 feet"
    arcpy.SelectLayerByLocation_management(templyr,"WITHIN_A_DISTANCE",geom,diststr,"NEW_SELECTION")
    result = arcpy.GetCount_management(templyr)
    fcount = int(result.getOutput(0))
    stvalue = ""
    stname = ""
#    regvalue = ""
    stfield = "ST_ABBREV"
#    regfield = "REGION"
    stnamefld = "STATE_NAME"
    if fcount > 0:
#        cursor = arcpy.SearchCursor(templyr,[stfield,stnamefld,regfield])
        cursor = arcpy.SearchCursor(templyr,[stfield,stnamefld])
        row = next(cursor)
        stvalue = row.getValue(stfield)
        stname = row.getValue(stnamefld)
#        regvalue = row.getValue(regfield)
        del cursor
    else:
        diststr = dx + " " + ux
        arcpy.SelectLayerByLocation_management(templyr,"WITHIN_A_DISTANCE",geom,diststr,"NEW_SELECTION")
        result = arcpy.GetCount_management(templyr)
        fcount = int(result.getOutput(0))
        if fcount > 0:
#            cursor = arcpy.SearchCursor(templyr,[stfield,stnamefld,regfield])
            cursor = arcpy.SearchCursor(templyr,[stfield,stnamefld])
            row = next(cursor)
            stvalue = row.getValue(stfield)
            stname = row.getValue(stnamefld)
#            regvalue = row.getValue(regfield)
            del cursor

#    return stvalue,stname,str(regvalue)
    return stvalue,stname

#def calPercentile(st,reg):
def calPercentile(st):
   
    stinput = ejws + "/States"
    wherestr ="REGION='" +  str(st) + "'"
    starr = arcpy.da.TableToNumPyArray(stinput,['*'],where_clause=wherestr)
    #arcpy.AddMessage("state array: " + str(len(starr)))
#    reginput = ejws + "/Regions"
#    regwherestr ="REGION='" +  str(reg) + "'"
#    regarr = arcpy.da.TableToNumPyArray(reginput,['*'],where_clause=regwherestr)
    #arcpy.AddMessage("region array: " + str(len(regarr)))

    usinput = ejws + "/USA"
    uswherestr ="1=1"
    usarr = arcpy.da.TableToNumPyArray(usinput,['*'],where_clause=uswherestr)
    #arcpy.AddMessage("USA array: " + str(len(usarr)))
    for fld in ejdataobj:
        if ejdataobj[fld]["hasvalue"]:
            fvalue = ejdataobj[fld]["raw_value"]
            fvalue_st = ejdataobj[fld]["raw_value_st"]


            getPercentile('state', fld, fvalue_st, starr)
#            getPercentile('region', fld, fvalue, regarr)
            getPercentile('nation', fld, fvalue, usarr)
        else:
            ejdataobj[fld]["stateavg"] = "N/A"
#            ejdataobj[fld]["regionavg"] = "N/A"
            ejdataobj[fld]["nationavg"] = "N/A"
            ejdataobj[fld]["statepctile"] = "N/A"
#            ejdataobj[fld]["regionpctile"] = "N/A"
            ejdataobj[fld]["nationpctile"] = "N/A"

#def calPercentile_PR(st,reg):
def calPercentile_PR(st):

    stinput = ejws + "/States"
    wherestr ="REGION='" +  str(st) + "'"
    starr = arcpy.da.TableToNumPyArray(stinput,['*'],where_clause=wherestr)


    for fld in ejdataobj:
        if ejdataobj[fld]["hasvalue"]:
            fvalue = ejdataobj[fld]["raw_value"]
            fvalue_st = ejdataobj[fld]["raw_value_st"]

            getPercentile('state', fld, fvalue_st, starr)
#            ejdataobj[fld]["regionavg"] = "N/A"
            ejdataobj[fld]["nationavg"] = "N/A"
#            ejdataobj[fld]["regionpctile"] = "N/A"
            ejdataobj[fld]["nationpctile"] = "N/A"
        else:
            ejdataobj[fld]["stateavg"] = "N/A"
#            ejdataobj[fld]["regionavg"] = "N/A"
            ejdataobj[fld]["nationavg"] = "N/A"
            ejdataobj[fld]["statepctile"] = "N/A"
#            ejdataobj[fld]["regionpctile"] = "N/A"
            ejdataobj[fld]["nationpctile"] = "N/A"

#def calAvgValue(st,reg):
def calAvgValue(st):
    
    stinput = "States"
    wherestr ="REGION='" +  str(st) + "'"
    starr = arcpy.da.TableToNumPyArray(stinput,['*'],where_clause=wherestr)
    #arcpy.AddMessage("state array: " + str(len(starr)))

#    reginput = "Regions"
#    regwherestr ="REGION='" +  str(reg) + "'"
#    regarr = arcpy.da.TableToNumPyArray(reginput,['*'],where_clause=regwherestr)
    #arcpy.AddMessage("region array: " + str(len(regarr)))

    usinput = "USA"
    uswherestr ="1=1"
    usarr = arcpy.da.TableToNumPyArray(usinput,['*'],where_clause=uswherestr)
    #arcpy.AddMessage("USA array: " + str(len(usarr)))

    for fld in ejdataobj:
        fvalue = "N/A"
        getPercentile('state', fld, fvalue, starr)
#        getPercentile('region', fld, fvalue, regarr)
        getPercentile('nation', fld, fvalue, usarr)


def calBGweight(gm):

    gmjson = gm.JSON
   
    jsonobj = {'geometry': gmjson, 'f': 'json', 'geometryType':	'esriGeometryPolygon',
    'groupByFieldsForStatistics':'STCNTRBG','inSR':4326,'outFields':'*',
    'outSR':4326,
    'outStatistics':[{"statisticType":"sum","onStatisticField":"POP_WEIGHT","outStatisticFieldName":"popweight"}],
    'returnGeometry':	'false',
    'spatialRel':	'esriSpatialRelIntersects'
    }




    serviceURL = ejconfig.bkurl
    try:
        params = urllib.parse.urlencode(jsonobj)
        

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        serverName = ejconfig.server

        # Connect to URL and post parameters
        httpConn = http.client.HTTPSConnection(serverName)
        httpConn.request("POST", serviceURL, params, headers)

        # Read response
        response = httpConn.getresponse()
        if (response.status != 200):
            httpConn.close()
            print ("Error while querying Service details.")
            return None
        else:
            data = response.read()

            # Check that data returned is not an error object
            if not assertJsonSuccess(data):
                print("Error returned by Service Query operation. " + data)
                return

            # Deserialize response into Python object
            dataObj = json.loads(data)
            httpConn.close()
            if not 'features' in dataObj:
                arcpy.AddMessage( "No record returned for query on '{0}'!".format(serviceURL))
                return None
            else:
                weightobj = {}
                fset = dataObj['features']
                for g in fset:
                    bg = g['attributes']['STCNTRBG']
                    pweight = g['attributes']['popweight']
                    #arcpy.AddMessage(str(bg) + ": " + str(pweight))
                    weightobj[bg] = pweight
                return weightobj
    except IOError:
        arcpy.AddWarning("Error occurred when accessing the EJSCREEN service.")
        arcpy.AddWarning("The service may be not available or you may not be online.")
        sys.exit()


def assertJsonSuccess(data):
 
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print("Error: JSON object returns an error. " + str(obj))
        return False
    else:
        return True

def constructHASH():
   
    try:
        lookupresturl = ejconfig.querylookupbase + "FOR_DATA%3D%27Y%27"
        lookres = urllib.request.urlopen(lookupresturl)
        lookstr = lookres.read()
        lookjson = json.loads(lookstr)
        lookres.close()
        
        fobj = lookjson["features"]
        
        
        fieldsArray = []
        for item in fobj:
            
            fldname =item["attributes"]["FIELD_NAME"]
            pdfname = item["attributes"]["PDF_NAME"]
            basedesc = item["attributes"]["CSV_NAME"]
            indexcode = item["attributes"]["IndexCode"]
            formatter = item["attributes"]["FORMATTER"]
            isnata = item["attributes"]["IS_NATA"]
            denominator = item["attributes"]["DENOMINATOR"]
            ejdataobj[fldname]= {"pdfname": pdfname,"desc": basedesc,"contenttype": indexcode,"formatter": formatter, "isnata": isnata, "denominator": denominator}

            if indexcode == "P_EJ2" or indexcode == "P_EJ5":

                ejdataobj[fldname]["rawdata"] = "no"
            else:

                ejdataobj[fldname]["rawdata"] = "yes"
            fieldsArray.append(fldname)
        ejdataobj["DEMOGIDX_2"]["formatter"] = "2"
        ejdataobj["DEMOGIDX_5"]["formatter"] = "2"
        return fieldsArray
    except IOError:
        #arcpy.AddError("Error occurred when getting EJSCREEN lookup table.")
        arcpy.AddError("Error occured when accessing the EJSCREEN service.")
        #arcpy.AddError("EJSCREEN map service '{0}' may be down.".format(ejconfig.lookupurl))
        arcpy.AddError("The service or your computer may be offline.")
        sys.exit()

def getPercentile(level, fname, fvalue, feats):
  
    #arcpy.AddMessage("state: " + level + "; "  + fname + "; " + str(fvalue) + "; " + str(math.isnan(fvalue)))
    if fvalue == 'N/A':
        ejdataobj[fname][level + "pctile"] = "N/A"
        for r in feats:
            rvalue = r[fname]
            if math.isnan(rvalue):
                rvalue = "N/A"
            ptilevalue = (r["PCTILE"]).strip()
            if ptilevalue == 'mean':
                ejdataobj[fname][level + "avg"] = rvalue
    elif math.isnan(fvalue):
        ejdataobj[fname][level + "pctile"] = "N/A"
        for r in feats:
            rvalue = r[fname]
            if math.isnan(rvalue):
                rvalue = "N/A"
            ptilevalue = (r["PCTILE"]).strip()
            if ptilevalue == 'mean':
                ejdataobj[fname][level + "avg"] = rvalue
    else:
        valueArray = {}
        for r in feats:
            rvalue = r[fname]
            #arcpy.AddMessage("rvalue: '" + str(rvalue) + "'")
            if math.isnan(rvalue):
                rvalue = "N/A"
            ptilevalue = (r["PCTILE"]).strip()
            #arcpy.AddMessage("pcttile: '" + str(ptilevalue) + "'; flvalue: '" + str(rvalue) + "'; " + str(ptilevalue.isdigit()))
            if ptilevalue == 'mean':
                ejdataobj[fname][level + "avg"] = rvalue
            elif ptilevalue.isdigit():
                intptile = int(ptilevalue)
                valueArray[intptile] = rvalue
                #arcpy.AddMessage("pcttile: " + str(intptile) + "; flvalue: " + str(rvalue))

        prevalue = valueArray[0]
        curptile= 0
        hasvalue = False
        ##sorted(valueArray, key=valueArray.get)
        
        for i in valueArray:
            rowvalue = valueArray[i]
        
            if rowvalue == "N/A":
                hasvalue = True
                ejdataobj[fname][level + "pctile"] = "N/A"
            else:

                if i > 0:
                    prevalue = valueArray[i-1]
                if rowvalue >= fvalue:
                    if rowvalue == fvalue:
                        curptile = i
                        ejdataobj[fname][level + "pctile"] = curptile
                        hasvalue = True
                        break
                    else:
                        curptile = i-1
                    if i == 0:
                        curptile = 0
                    ejdataobj[fname][level + "pctile"] = curptile
                    hasvalue = True
                    break
##        if level == "nation" and fname == "DSLPM":
##            arcpy.AddMessage(fname + ": " + str(fvalue) + "; " + str(ejdataobj[fname][level + "pctile"]))
        if not hasvalue:
            ejdataobj[fname][level + "pctile"] = 100
        if level == "state" and (fname == "D2_PWDIS" or fname == "D5_PWDIS" or fname == "PWDIS") and fvalue == 0:
            ejdataobj[fname][level + "pctile"] = "N/A";

def getNATApctText(inpct):

    outpcttext = ""
    if inpct == "N/A":
        outpcttext = "N/A"
    elif (inpct >= 95):
        outpcttext = "95-100th";
    elif ((inpct >= 90) and (inpct < 95)):
        outpcttext = "90-95th"
    elif ((inpct >= 80) and (inpct < 90)):
        outpcttext = "80-90th"
    elif ((inpct >= 70) and (inpct < 80)):
        outpcttext = "70-80th"
    elif ((inpct >= 60) and (inpct < 70)):
        outpcttext = "60-70th"
    elif ((inpct >= 50) and (inpct < 60)):
        outpcttext = "50-60th"
    elif ((inpct >= 0) and (inpct < 50)):
        outpcttext = "<50th"
    return outpcttext

def getEnvText(invalue,digsig):

    if invalue == 'N/A':
        v = invalue
    else:
        invalue = float(invalue)
        if math.isnan(invalue):
            v = 'N/A'
        else:
            digsig = int(digsig)

            invaluestr = str(roundNumber(invalue,0))

            dint = len(invaluestr)

            v = 0
            if invalue > 0:
                if dint <= 2:
                    dig = digsig -1 - int(math.floor(math.log(abs(invalue)) / math.log(10)))
                    v=round(invalue,dig)
                else:
                    m = dint - digsig
                    v = roundNumber(invalue/pow(10,m),0)*pow(10,m)
                    ##v = roundNumber(invalue,m)
    return v

def roundNumber(num,dec):

    result = round(num * pow(10, dec)) / pow(10, dec)
    return int(result)

if __name__ == '__main__':
    fc = arcpy.GetParameterAsText(0)
    dx = arcpy.GetParameterAsText(1)
    ux = arcpy.GetParameterAsText(2)
    ejws = arcpy.GetParameterAsText(3)
    outFC = arcpy.GetParameterAsText(4)
    newdx = dx.strip()
    arcpy.env.workspace = ejws
#    if (arcpy.Exists("EJSCREEN_Primary") or arcpy.Exists("EJSCREEN_Full_with_AS_CNMI_GU_VI")) and arcpy.Exists("States") and arcpy.Exists("Regions") and arcpy.Exists("USA") :
    if (arcpy.Exists("EJSCREEN_Primary") or arcpy.Exists("EJSCREEN_Full_with_AS_CNMI_GU_VI")) and arcpy.Exists("States") and arcpy.Exists("USA") :  
        ejdataobj = {}
        desc = arcpy.Describe(fc)
        if desc.shapeType == "Point":
            if arcpy.Exists("EJSCREEN_Primary"):
                ejFields = arcpy.ListFields(ejws+"/EJSCREEN_Primary")
            elif arcpy.Exists("EJSCREEN_Full_with_AS_CNMI_GU_VI"):
                ejFields = arcpy.ListFields(ejws+"/EJSCREEN_Full_with_AS_CNMI_GU_VI")
            if checkfield("NEURO",ejFields):
                arcpy.AddWarning("Your EJSCREEN fgdb data is in older version (v4 or v2017). This tool only processes the EJSCREEN V2020 fgdb data.")
            else:
                main(fc,newdx,ux, ejws,outFC)

            ##outFC = arcpy.SetParameterAsText(4,foldername)
        else:
            arcpy.AddWarning("You need to input point feature class. The input feature class is '" + desc.shapeType + "'")
    else:
        arcpy.AddError("EJSCREEN_Primary or EJSCREEN_Full, States, Regions or USA doesn't exist in '" + ejws + "'. Please check your gdb folder!")