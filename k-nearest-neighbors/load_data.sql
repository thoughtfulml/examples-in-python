drop table if exists house_sales;
CREATE TABLE house_sales (
  tax_id bigserial primary key,
  sale_date date not null,
  plat_id int,
  sale_price decimal(10,2),
  tax_value decimal(10,2)
);

drop table IF EXISTS  house_sales_tmp;
CREATE TABLE house_sales_tmp
(
 "ExciseTaxNbr" bigserial,
 "Major" integer,
 "Minor" integer,
 "DocumentDate" date,
 "SalePrice" numeric(11,2),
 "RecordingNbr" varchar(255),
 "Volume" varchar(255),
 "Page" varchar(255),
 "PlatNbr" varchar(255),
 "PlatType" varchar(255),
 "PlatLot" varchar(255),
 "PlatBlock" varchar(255),
 "SellerName" varchar(255),
 "BuyerName" varchar(255),
 "PropertyType" varchar(255),
 "PrincipalUse" varchar(255),
 "SaleInstrument" varchar(255),
 "AFForestLand" varchar(255),
 "AFCurrentUseLand" varchar(255),
 "AFNonProfitUse" varchar(255),
 "AFHistoricProperty" varchar(255),
 "SaleReason" varchar(255),
 "PropertyClass" varchar(255),
 "SaleWarning" varchar(255));
\COPY house_sales_tmp FROM '/home/hexgnu/git/examples-in-python/k-nearest-neighbors/EXTR_RPSale.csv' DELIMITERS ',' CSV HEADER;

DELETE FROM house_sales_tmp WHERE "DocumentDate" < '2015-01-01';
CREATE INDEX house_sales_blap ON house_sales_tmp ("Major", "Minor");

drop table if exists house_parcel_tmp;
CREATE TABLE house_parcel_tmp (
"Major" integer
,"Minor" integer
,"PropName" varchar(255)
,"PlatName" varchar(255)
,"PlatLot" varchar(255)
,"PlatBlock" varchar(255)
,"Range" varchar(255)
,"Township" varchar(255)
,"Section" varchar(255)
,"QuarterSection" varchar(255)
,"PropType" varchar(255)
,"Area" varchar(255)
,"SubArea" varchar(255)
,"DistrictName" varchar(255)
,"LevyCode" varchar(255)
,"CurrentZoning" varchar(255)
,"HBUAsIfVacant" varchar(255)
,"HBUAsImproved" varchar(255)
,"PresentUse" varchar(255)
,"SqFtLot" varchar(255)
,"WaterSystem" varchar(255)
,"SewerSystem" varchar(255)
,"Access" varchar(255)
,"Topography" varchar(255)
,"StreetSurface" varchar(255)
,"RestrictiveSzShape" varchar(255)
,"InadequateParking" varchar(255)
,"PcntUnusable" varchar(255)
,"MtRainier" varchar(255)
,"Olympics" varchar(255)
,"Cascades" varchar(255)
,"Territorial" varchar(255)
,"SeattleSkyline" varchar(255)
,"PugetSound" varchar(255)
,"LakeWashington" varchar(255)
,"LakeSammamish" varchar(255)
,"SmallLakeRiverCreek" varchar(255)
,"OtherView" varchar(255)
,"WfntLocation" varchar(255)
,"WfntFootage" varchar(255)
,"WfntBank" varchar(255)
,"WfntPoorQuality" varchar(255)
,"WfntRestrictedAccess" varchar(255)
,"WfntAccessRights" varchar(255)
,"WfntProximityInfluence" varchar(255)
,"TidelandShoreland" varchar(255)
,"LotDepthFactor" varchar(255)
,"TrafficNoise" varchar(255)
,"AirportNoise" varchar(255)
,"PowerLines" varchar(255)
,"OtherNuisances" varchar(255)
,"NbrBldgSites" varchar(255)
,"Contamination" varchar(255)
,"DNRLease" varchar(255)
,"AdjacentGolfFairway" varchar(255)
,"AdjacentGreenbelt" varchar(255)
,"CommonProperty" varchar(255)
,"HistoricSite" varchar(255)
,"CurrentUseDesignation" varchar(255)
,"NativeGrowthProtEsmt" varchar(255)
,"Easements" varchar(255)
,"OtherDesignation" varchar(255)
,"DeedRestrictions" varchar(255)
,"DevelopmentRightsPurch" varchar(255)
,"CoalMineHazard" varchar(255)
,"CriticalDrainage" varchar(255)
,"ErosionHazard" varchar(255)
,"LandfillBuffer" varchar(255)
,"HundredYrFloodPlain" varchar(255)
,"SeismicHazard" varchar(255)
,"LandslideHazard" varchar(255)
,"SteepSlopeHazard" varchar(255)
,"Stream" varchar(255)
,"Wetland" varchar(255)
,"SpeciesOfConcern" varchar(255)
,"SensitiveAreaTract" varchar(255)
,"WaterProblems" varchar(255)
,"TranspConcurrency" varchar(255)
,"OtherProblems" varchar(255)
);

\COPY house_parcel_tmp FROM '/home/hexgnu/git/examples-in-python/k-nearest-neighbors/EXTR_Parcel.csv' DELIMITERS ',' CSV HEADER;

CREATE INDEX house_parcel_blap ON house_parcel_tmp ("Major", "Minor");

DROP TABLE house_taxes_tmp;
CREATE TABLE house_taxes_tmp (
  "AcctNbr" varchar(255),
  "Major" integer,
  "Minor" integer,
  "AttnLine" varchar(255),
  "AddrLine" varchar(255),
  "CityState" varchar(255),
  "ZipCode" varchar(255),
  "LevyCode" varchar(255),
  "TaxStat" varchar(255),
  "BillYr" integer,
  "NewConstructionFlag" varchar(255),
  "TaxValReason" varchar(255),
  "ApprLandVal" numeric(11,2),
  "ApprImpsVal" numeric(11,2),
  "TaxableLandVal" numeric(11,2),
  "TaxableImpsVal" numeric(11,2)
);

\COPY house_taxes_tmp FROM '/home/hexgnu/git/examples-in-python/k-nearest-neighbors/EXTR_RPAcct_NoName.csv' DELIMITERS ',' CSV HEADER;

CREATE INDEX house_taxes_blap ON house_taxes_tmp ("Major", "Minor");

DELETE FROM house_taxes_tmp WHERE "BillYr" < 2015;

DROP TABLE IF EXISTS house_location_tmp;
CREATE TABLE house_location_tmp (
  "Major" integer
  , "Minor" integer
  , "BldgNbr" varchar(255)
  , "NbrLivingUnits" varchar(255)
  , "Address" varchar(255)
  , "BuildingNumber" varchar(255)
  , "Fraction" varchar(255)
  , "DirectionPrefix" varchar(255)
  , "StreetName" varchar(255)
  , "StreetType" varchar(255)
  , "DirectionSuffix" varchar(255)
  , "ZipCode" varchar(255)
  , "Stories" varchar(255)
  , "BldgGrade" varchar(255)
  , "BldgGradeVar" varchar(255)
  , "SqFt1stFloor" varchar(255)
  , "SqFtHalfFloor" varchar(255)
  , "SqFt2ndFloor" varchar(255)
  , "SqFtUpperFloor" varchar(255)
  , "SqFtUnfinFull" varchar(255)
  , "SqFtUnfinHalf" varchar(255)
  , "SqFtTotLiving" varchar(255)
  , "SqFtTotBasement" varchar(255)
  , "SqFtFinBasement" varchar(255)
  , "FinBasementGrade" varchar(255)
  , "SqFtGarageBasement" varchar(255)
  , "SqFtGarageAttached" varchar(255)
  , "DaylightBasement" varchar(255)
  , "SqFtOpenPorch" varchar(255)
  , "SqFtEnclosedPorch" varchar(255)
  , "SqFtDeck" varchar(255)
  , "HeatSystem" varchar(255)
  , "HeatSource" varchar(255)
  , "BrickStone" varchar(255)
  , "ViewUtilization" varchar(255)
  , "Bedrooms" varchar(255)
  , "BathHalfCount" varchar(255)
  , "Bath3qtrCount" varchar(255)
  , "BathFullCount" varchar(255)
  , "FpSingleStory" varchar(255)
  , "FpMultiStory" varchar(255)
  , "FpFreestanding" varchar(255)
  , "FpAdditional" varchar(255)
  , "YrBuilt" varchar(255)
  , "YrRenovated" varchar(255)
  , "PcntComplete" varchar(255)
  , "Obsolescence" varchar(255)
  , "PcntNetCondition" varchar(255)
  , "Condition" varchar(255)
  , "AddnlCost" varchar(255)
);
\COPY house_location_tmp FROM '/home/hexgnu/git/examples-in-python/k-nearest-neighbors/EXTR_ResBldg.csv' DELIMITERS ',' CSV HEADER;


CREATE INDEX house_location_tmp_major_minor ON house_location_tmp ("Major", "Minor");
