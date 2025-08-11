#### Where the data came from
##### Landcover
[original link I used](https://www.mrlc.gov/data/nlcd-2021-land-cover-conus) no longer working, but is available from [datacommons.cyverse.org](https://de.cyverse.org/anon-files/iplant/home/shared/atur/Urban/NLCD%202021/nlcd_2021_land_cover_l48_20230630.img), which seems to be just some account someone made to upload a bunch of data. Filename: `nlcd_2021_land_cover_l48_20230630.img`

Currently they want you to use [www.mrlc.gov/data](https://www.mrlc.gov/data) . Select Conus, 2023, and then try to download Land Cover (CONUS).

There's a [possibly newer landcover geotiff](https://www.mrlc.gov/downloads/sciweb1/shared/mrlc/data-bundles/Annual_NLCD_LndCov_2023_CU_C1V0.tif) available ([metadata](https://www.mrlc.gov/downloads/sciweb1/shared/mrlc/metadata/Annual_NLCD_LndCov_2023_CU_C1V0.xml)). You can reproject it to EPSG:5070 in a similar way (see New reprojection) below.

##### Elevation
I have a long list of links that I seem to have read out of a csv file that I think I got from Andrew, who probably got it from the USGS webviewer. Links seem to still work. I downloaded each file and then did

```zsh
gdalbuildvrt merged.vrt *.tif 
```
###### Elevation files

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w081/USGS_1_n26w081_20231221.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w082/USGS_1_n26w082_20231221.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w081/USGS_1_n27w081_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w082/USGS_1_n27w082_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w083/USGS_1_n27w083_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w099/USGS_1_n27w099_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w081/USGS_1_n28w081_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w082/USGS_1_n28w082_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w083/USGS_1_n28w083_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w099/USGS_1_n28w099_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w100/USGS_1_n28w100_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w081/USGS_1_n29w081_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w082/USGS_1_n29w082_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w083/USGS_1_n29w083_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w090/USGS_1_n29w090_20231213.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w096/USGS_1_n29w096_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w097/USGS_1_n29w097_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w098/USGS_1_n29w098_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w099/USGS_1_n29w099_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w100/USGS_1_n29w100_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w101/USGS_1_n29w101_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w104/USGS_1_n29w104_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w081/USGS_1_n30w081_20221019.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w082/USGS_1_n30w082_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w083/USGS_1_n30w083_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w084/USGS_1_n30w084_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w085/USGS_1_n30w085_20221017.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w086/USGS_1_n30w086_20221017.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w090/USGS_1_n30w090_20231213.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w091/USGS_1_n30w091_20231213.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w092/USGS_1_n30w092_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w093/USGS_1_n30w093_20220831.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w094/USGS_1_n30w094_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w095/USGS_1_n30w095_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w096/USGS_1_n30w096_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w097/USGS_1_n30w097_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w098/USGS_1_n30w098_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w099/USGS_1_n30w099_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w100/USGS_1_n30w100_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w101/USGS_1_n30w101_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w102/USGS_1_n30w102_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w103/USGS_1_n30w103_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w104/USGS_1_n30w104_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w105/USGS_1_n30w105_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w082/USGS_1_n31w082_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w083/USGS_1_n31w083_20221103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w084/USGS_1_n31w084_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w085/USGS_1_n31w085_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w086/USGS_1_n31w086_20230306.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w087/USGS_1_n31w087_20230306.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w088/USGS_1_n31w088_20240502.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w089/USGS_1_n31w089_20240502.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w090/USGS_1_n31w090_20231213.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w091/USGS_1_n31w091_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w092/USGS_1_n31w092_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w093/USGS_1_n31w093_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w094/USGS_1_n31w094_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w095/USGS_1_n31w095_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w096/USGS_1_n31w096_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w097/USGS_1_n31w097_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w098/USGS_1_n31w098_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w099/USGS_1_n31w099_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w100/USGS_1_n31w100_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w101/USGS_1_n31w101_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w102/USGS_1_n31w102_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w103/USGS_1_n31w103_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w104/USGS_1_n31w104_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w105/USGS_1_n31w105_20210616.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w106/USGS_1_n31w106_20210616.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w081/USGS_1_n32w081_20220725.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w082/USGS_1_n32w082_20220725.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w083/USGS_1_n32w083_20220725.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w084/USGS_1_n32w084_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w085/USGS_1_n32w085_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w086/USGS_1_n32w086_20230306.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w087/USGS_1_n32w087_20230306.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w088/USGS_1_n32w088_20240502.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w089/USGS_1_n32w089_20240502.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w090/USGS_1_n32w090_20220601.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w091/USGS_1_n32w091_20220601.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w092/USGS_1_n32w092_20230609.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w093/USGS_1_n32w093_20230609.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w094/USGS_1_n32w094_20211115.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w095/USGS_1_n32w095_20211115.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w096/USGS_1_n32w096_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w097/USGS_1_n32w097_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w098/USGS_1_n32w098_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w099/USGS_1_n32w099_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w100/USGS_1_n32w100_20211103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w102/USGS_1_n32w102_20201228.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w103/USGS_1_n32w103_20211124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w104/USGS_1_n32w104_20220721.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w105/USGS_1_n32w105_20220721.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w106/USGS_1_n32w106_20220721.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w107/USGS_1_n32w107_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w108/USGS_1_n32w108_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w109/USGS_1_n32w109_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w110/USGS_1_n32w110_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w111/USGS_1_n32w111_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w112/USGS_1_n32w112_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w113/USGS_1_n32w113_20210615.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w114/USGS_1_n32w114_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w080/USGS_1_n33w080_20220504.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w081/USGS_1_n33w081_20220725.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w082/USGS_1_n33w082_20220725.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w083/USGS_1_n33w083_20220725.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w084/USGS_1_n33w084_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w085/USGS_1_n33w085_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w086/USGS_1_n33w086_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w087/USGS_1_n33w087_20220728.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w088/USGS_1_n33w088_20240502.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w089/USGS_1_n33w089_20240502.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w090/USGS_1_n33w090_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w091/USGS_1_n33w091_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w092/USGS_1_n33w092_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w093/USGS_1_n33w093_20230609.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w094/USGS_1_n33w094_20230609.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w095/USGS_1_n33w095_20211115.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w096/USGS_1_n33w096_20211124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w097/USGS_1_n33w097_20211124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w098/USGS_1_n33w098_20211124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w099/USGS_1_n33w099_20211124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w103/USGS_1_n33w103_20211124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w104/USGS_1_n33w104_20220721.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w105/USGS_1_n33w105_20220721.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w106/USGS_1_n33w106_20220721.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w107/USGS_1_n33w107_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w108/USGS_1_n33w108_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w109/USGS_1_n33w109_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w110/USGS_1_n33w110_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w111/USGS_1_n33w111_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w112/USGS_1_n33w112_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w113/USGS_1_n33w113_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w114/USGS_1_n33w114_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w115/USGS_1_n33w115_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w116/USGS_1_n33w116_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w117/USGS_1_n33w117_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w080/USGS_1_n34w080_20220504.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w081/USGS_1_n34w081_20220504.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w082/USGS_1_n34w082_20220725.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w083/USGS_1_n34w083_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w084/USGS_1_n34w084_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w085/USGS_1_n34w085_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w086/USGS_1_n34w086_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w087/USGS_1_n34w087_20220728.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w088/USGS_1_n34w088_20240502.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w089/USGS_1_n34w089_20220601.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w090/USGS_1_n34w090_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w091/USGS_1_n34w091_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w092/USGS_1_n34w092_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w093/USGS_1_n34w093_20230609.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w094/USGS_1_n34w094_20230609.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w095/USGS_1_n34w095_20211115.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w097/USGS_1_n34w097_20211124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w098/USGS_1_n34w098_20211124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w099/USGS_1_n34w099_20211124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w104/USGS_1_n34w104_20220721.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w105/USGS_1_n34w105_20220721.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w106/USGS_1_n34w106_20220721.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w107/USGS_1_n34w107_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w108/USGS_1_n34w108_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w109/USGS_1_n34w109_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w110/USGS_1_n34w110_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w111/USGS_1_n34w111_20240402.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w112/USGS_1_n34w112_20240402.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w113/USGS_1_n34w113_20240402.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w114/USGS_1_n34w114_20240402.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w115/USGS_1_n34w115_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w116/USGS_1_n34w116_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w117/USGS_1_n34w117_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w080/USGS_1_n35w080_20240611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w081/USGS_1_n35w081_20240611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w082/USGS_1_n35w082_20220504.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w083/USGS_1_n35w083_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w084/USGS_1_n35w084_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w085/USGS_1_n35w085_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w086/USGS_1_n35w086_20220728.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w087/USGS_1_n35w087_20220728.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w088/USGS_1_n35w088_20220728.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w089/USGS_1_n35w089_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w090/USGS_1_n35w090_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w091/USGS_1_n35w091_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w092/USGS_1_n35w092_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w104/USGS_1_n35w104_20210624.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w105/USGS_1_n35w105_20220801.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w106/USGS_1_n35w106_20220801.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w107/USGS_1_n35w107_20231208.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w108/USGS_1_n35w108_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w109/USGS_1_n35w109_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w110/USGS_1_n35w110_20240606.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w111/USGS_1_n35w111_20240402.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w112/USGS_1_n35w112_20240402.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w113/USGS_1_n35w113_20240402.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w114/USGS_1_n35w114_20240402.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w115/USGS_1_n35w115_20221019.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w116/USGS_1_n35w116_20221019.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w117/USGS_1_n35w117_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w118/USGS_1_n35w118_20221019.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w119/USGS_1_n35w119_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w120/USGS_1_n35w120_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w121/USGS_1_n35w121_20210301.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w080/USGS_1_n36w080_20240611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w081/USGS_1_n36w081_20240611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w082/USGS_1_n36w082_20240611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w083/USGS_1_n36w083_20220512.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w084/USGS_1_n36w084_20220725.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w085/USGS_1_n36w085_20220725.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w086/USGS_1_n36w086_20220729.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w087/USGS_1_n36w087_20230130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w088/USGS_1_n36w088_20230130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w089/USGS_1_n36w089_20220729.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w090/USGS_1_n36w090_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w091/USGS_1_n36w091_20221121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w098/USGS_1_n36w098_20210623.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w104/USGS_1_n36w104_20210624.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w105/USGS_1_n36w105_20220801.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w106/USGS_1_n36w106_20220801.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w107/USGS_1_n36w107_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w108/USGS_1_n36w108_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w109/USGS_1_n36w109_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w110/USGS_1_n36w110_20240606.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w111/USGS_1_n36w111_20220303.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w112/USGS_1_n36w112_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w113/USGS_1_n36w113_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w114/USGS_1_n36w114_20240402.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w115/USGS_1_n36w115_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w116/USGS_1_n36w116_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w117/USGS_1_n36w117_20221019.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w118/USGS_1_n36w118_20221019.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w119/USGS_1_n36w119_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w120/USGS_1_n36w120_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w121/USGS_1_n36w121_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w122/USGS_1_n36w122_20210301.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w077/USGS_1_n37w077_20211220.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w078/USGS_1_n37w078_20210610.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w079/USGS_1_n37w079_20210305.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w080/USGS_1_n37w080_20210305.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w081/USGS_1_n37w081_20240611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w082/USGS_1_n37w082_20240611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w083/USGS_1_n37w083_20220512.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w087/USGS_1_n37w087_20230407.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w088/USGS_1_n37w088_20230407.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w089/USGS_1_n37w089_20230123.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w090/USGS_1_n37w090_20231226.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w091/USGS_1_n37w091_20240408.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w092/USGS_1_n37w092_20240408.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w093/USGS_1_n37w093_20231226.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w094/USGS_1_n37w094_20231226.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w095/USGS_1_n37w095_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w096/USGS_1_n37w096_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w097/USGS_1_n37w097_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w099/USGS_1_n37w099_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w100/USGS_1_n37w100_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w101/USGS_1_n37w101_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w102/USGS_1_n37w102_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w103/USGS_1_n37w103_20210623.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w104/USGS_1_n37w104_20210623.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w105/USGS_1_n37w105_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w106/USGS_1_n37w106_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w107/USGS_1_n37w107_20220801.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w108/USGS_1_n37w108_20220801.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w109/USGS_1_n37w109_20220720.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w110/USGS_1_n37w110_20240606.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w111/USGS_1_n37w111_20240606.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w112/USGS_1_n37w112_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w113/USGS_1_n37w113_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w114/USGS_1_n37w114_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w115/USGS_1_n37w115_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w116/USGS_1_n37w116_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w119/USGS_1_n37w119_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w120/USGS_1_n37w120_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w121/USGS_1_n37w121_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w122/USGS_1_n37w122_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w123/USGS_1_n37w123_20210617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w076/USGS_1_n38w076_20220713.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w077/USGS_1_n38w077_20220713.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w078/USGS_1_n38w078_20211220.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w079/USGS_1_n38w079_20211229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w080/USGS_1_n38w080_20211229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w081/USGS_1_n38w081_20230816.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w082/USGS_1_n38w082_20230816.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w083/USGS_1_n38w083_20230816.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w084/USGS_1_n38w084_20230123.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w085/USGS_1_n38w085_20220311.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w086/USGS_1_n38w086_20230407.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w087/USGS_1_n38w087_20230407.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w088/USGS_1_n38w088_20230407.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w089/USGS_1_n38w089_20220318.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w090/USGS_1_n38w090_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w091/USGS_1_n38w091_20240408.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w092/USGS_1_n38w092_20240408.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w093/USGS_1_n38w093_20231226.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w094/USGS_1_n38w094_20240408.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w095/USGS_1_n38w095_20240408.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w096/USGS_1_n38w096_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w097/USGS_1_n38w097_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w098/USGS_1_n38w098_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w099/USGS_1_n38w099_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w100/USGS_1_n38w100_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w101/USGS_1_n38w101_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w102/USGS_1_n38w102_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w103/USGS_1_n38w103_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w104/USGS_1_n38w104_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w105/USGS_1_n38w105_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w106/USGS_1_n38w106_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w107/USGS_1_n38w107_20220720.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w108/USGS_1_n38w108_20220720.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w109/USGS_1_n38w109_20220720.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w110/USGS_1_n38w110_20240606.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w111/USGS_1_n38w111_20211215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w112/USGS_1_n38w112_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w113/USGS_1_n38w113_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w114/USGS_1_n38w114_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w115/USGS_1_n38w115_20240614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w118/USGS_1_n38w118_20230308.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w119/USGS_1_n38w119_20230308.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w120/USGS_1_n38w120_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w121/USGS_1_n38w121_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w122/USGS_1_n38w122_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w123/USGS_1_n38w123_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w075/USGS_1_n39w075_20210624.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w076/USGS_1_n39w076_20220713.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w077/USGS_1_n39w077_20220713.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w078/USGS_1_n39w078_20220524.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w079/USGS_1_n39w079_20211229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w080/USGS_1_n39w080_20230816.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w081/USGS_1_n39w081_20230816.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w082/USGS_1_n39w082_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w083/USGS_1_n39w083_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w084/USGS_1_n39w084_20220311.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w085/USGS_1_n39w085_20230407.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w086/USGS_1_n39w086_20230407.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w087/USGS_1_n39w087_20230407.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w088/USGS_1_n39w088_20221205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w089/USGS_1_n39w089_20221205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w090/USGS_1_n39w090_20221205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w091/USGS_1_n39w091_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w092/USGS_1_n39w092_20240408.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w093/USGS_1_n39w093_20230117.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w094/USGS_1_n39w094_20240408.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w095/USGS_1_n39w095_20240408.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w096/USGS_1_n39w096_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w097/USGS_1_n39w097_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w098/USGS_1_n39w098_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w099/USGS_1_n39w099_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w100/USGS_1_n39w100_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w101/USGS_1_n39w101_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w102/USGS_1_n39w102_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w103/USGS_1_n39w103_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w104/USGS_1_n39w104_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w105/USGS_1_n39w105_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w106/USGS_1_n39w106_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w107/USGS_1_n39w107_20220331.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w108/USGS_1_n39w108_20220720.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w109/USGS_1_n39w109_20211208.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w110/USGS_1_n39w110_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w111/USGS_1_n39w111_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w112/USGS_1_n39w112_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w113/USGS_1_n39w113_20220510.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w114/USGS_1_n39w114_20220510.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w115/USGS_1_n39w115_20211215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w118/USGS_1_n39w118_20230308.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w119/USGS_1_n39w119_20230308.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w120/USGS_1_n39w120_20230308.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w121/USGS_1_n39w121_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w122/USGS_1_n39w122_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w123/USGS_1_n39w123_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w075/USGS_1_n40w075_20210624.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w076/USGS_1_n40w076_20220524.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w077/USGS_1_n40w077_20220524.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w078/USGS_1_n40w078_20230620.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w079/USGS_1_n40w079_20230816.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w080/USGS_1_n40w080_20230816.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w081/USGS_1_n40w081_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w082/USGS_1_n40w082_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w083/USGS_1_n40w083_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w085/USGS_1_n40w085_20230407.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w086/USGS_1_n40w086_20210617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w087/USGS_1_n40w087_20210617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w088/USGS_1_n40w088_20221205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w089/USGS_1_n40w089_20240104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w090/USGS_1_n40w090_20230303.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w091/USGS_1_n40w091_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w092/USGS_1_n40w092_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w093/USGS_1_n40w093_20240710.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w094/USGS_1_n40w094_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w095/USGS_1_n40w095_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w096/USGS_1_n40w096_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w097/USGS_1_n40w097_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w098/USGS_1_n40w098_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w099/USGS_1_n40w099_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w100/USGS_1_n40w100_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w101/USGS_1_n40w101_20220415.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w102/USGS_1_n40w102_20220415.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w103/USGS_1_n40w103_20211005.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w104/USGS_1_n40w104_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w105/USGS_1_n40w105_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w106/USGS_1_n40w106_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w107/USGS_1_n40w107_20220216.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w108/USGS_1_n40w108_20211208.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w110/USGS_1_n40w110_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w111/USGS_1_n40w111_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w112/USGS_1_n40w112_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w113/USGS_1_n40w113_20220510.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w114/USGS_1_n40w114_20220510.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w115/USGS_1_n40w115_20211101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w118/USGS_1_n40w118_20230308.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w119/USGS_1_n40w119_20230308.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w120/USGS_1_n40w120_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w121/USGS_1_n40w121_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w122/USGS_1_n40w122_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w123/USGS_1_n40w123_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w124/USGS_1_n40w124_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w074/USGS_1_n41w074_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w075/USGS_1_n41w075_20221115.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w076/USGS_1_n41w076_20221115.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w077/USGS_1_n41w077_20220429.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w078/USGS_1_n41w078_20220429.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w079/USGS_1_n41w079_20220429.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w080/USGS_1_n41w080_20210630.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w081/USGS_1_n41w081_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w082/USGS_1_n41w082_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w083/USGS_1_n41w083_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w084/USGS_1_n41w084_20230717.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w085/USGS_1_n41w085_20230717.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w086/USGS_1_n41w086_20210617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w087/USGS_1_n41w087_20210617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w088/USGS_1_n41w088_20221205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w089/USGS_1_n41w089_20240104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w090/USGS_1_n41w090_20240104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w091/USGS_1_n41w091_20240104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w092/USGS_1_n41w092_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w093/USGS_1_n41w093_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w094/USGS_1_n41w094_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w095/USGS_1_n41w095_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w096/USGS_1_n41w096_20240229.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w097/USGS_1_n41w097_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w098/USGS_1_n41w098_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w099/USGS_1_n41w099_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w100/USGS_1_n41w100_20230613.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w101/USGS_1_n41w101_20220415.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w102/USGS_1_n41w102_20220415.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w103/USGS_1_n41w103_20220415.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w104/USGS_1_n41w104_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w105/USGS_1_n41w105_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w106/USGS_1_n41w106_20230314.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w107/USGS_1_n41w107_20230314.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w108/USGS_1_n41w108_20230314.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w109/USGS_1_n41w109_20220805.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w110/USGS_1_n41w110_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w111/USGS_1_n41w111_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w112/USGS_1_n41w112_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w113/USGS_1_n41w113_20220510.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w114/USGS_1_n41w114_20220510.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w115/USGS_1_n41w115_20220510.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w116/USGS_1_n41w116_20231227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w117/USGS_1_n41w117_20231227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w118/USGS_1_n41w118_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w119/USGS_1_n41w119_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w120/USGS_1_n41w120_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w121/USGS_1_n41w121_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w122/USGS_1_n41w122_20220103.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w123/USGS_1_n41w123_20210624.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w124/USGS_1_n41w124_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w125/USGS_1_n41w125_20240313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w070/USGS_1_n42w070_20230117.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w071/USGS_1_n42w071_20230117.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w072/USGS_1_n42w072_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w073/USGS_1_n42w073_20211109.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w074/USGS_1_n42w074_20230307.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w075/USGS_1_n42w075_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w076/USGS_1_n42w076_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w077/USGS_1_n42w077_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w078/USGS_1_n42w078_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w079/USGS_1_n42w079_20220429.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w080/USGS_1_n42w080_20220429.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w081/USGS_1_n42w081_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w082/USGS_1_n42w082_20230911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w083/USGS_1_n42w083_20230717.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w084/USGS_1_n42w084_20230717.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w085/USGS_1_n42w085_20230717.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w086/USGS_1_n42w086_20210617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w087/USGS_1_n42w087_20210617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w088/USGS_1_n42w088_20240104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w089/USGS_1_n42w089_20240104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w090/USGS_1_n42w090_20240104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w091/USGS_1_n42w091_20240104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w092/USGS_1_n42w092_20240104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w093/USGS_1_n42w093_20221218.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w094/USGS_1_n42w094_20221218.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w095/USGS_1_n42w095_20221218.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w096/USGS_1_n42w096_20221218.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w097/USGS_1_n42w097_20230210.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w098/USGS_1_n42w098_20230210.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w099/USGS_1_n42w099_20230210.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w100/USGS_1_n42w100_20220426.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w101/USGS_1_n42w101_20220426.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w102/USGS_1_n42w102_20220415.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w103/USGS_1_n42w103_20220415.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w104/USGS_1_n42w104_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w105/USGS_1_n42w105_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w106/USGS_1_n42w106_20230314.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w107/USGS_1_n42w107_20230314.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w108/USGS_1_n42w108_20230314.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w109/USGS_1_n42w109_20220805.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w110/USGS_1_n42w110_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w111/USGS_1_n42w111_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w112/USGS_1_n42w112_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w113/USGS_1_n42w113_20211101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w114/USGS_1_n42w114_20220510.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w115/USGS_1_n42w115_20231227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w116/USGS_1_n42w116_20231227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w117/USGS_1_n42w117_20231227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w118/USGS_1_n42w118_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w119/USGS_1_n42w119_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w120/USGS_1_n42w120_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w121/USGS_1_n42w121_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w122/USGS_1_n42w122_20210624.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w123/USGS_1_n42w123_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w124/USGS_1_n42w124_20210623.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w071/USGS_1_n43w071_20230117.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w072/USGS_1_n43w072_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w073/USGS_1_n43w073_20230117.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w074/USGS_1_n43w074_20230307.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w075/USGS_1_n43w075_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w076/USGS_1_n43w076_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w077/USGS_1_n43w077_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w078/USGS_1_n43w078_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w079/USGS_1_n43w079_20220429.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w080/USGS_1_n43w080_20211122.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w081/USGS_1_n43w081_20210630.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w085/USGS_1_n43w085_20220815.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w088/USGS_1_n43w088_20240709.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w089/USGS_1_n43w089_20240709.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w090/USGS_1_n43w090_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w091/USGS_1_n43w091_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w092/USGS_1_n43w092_20240125.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w093/USGS_1_n43w093_20221218.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w094/USGS_1_n43w094_20221218.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w095/USGS_1_n43w095_20221218.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w096/USGS_1_n43w096_20221218.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w097/USGS_1_n43w097_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w098/USGS_1_n43w098_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w099/USGS_1_n43w099_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w100/USGS_1_n43w100_20230210.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w101/USGS_1_n43w101_20220726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w102/USGS_1_n43w102_20220726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w103/USGS_1_n43w103_20220726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w104/USGS_1_n43w104_20220726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w105/USGS_1_n43w105_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w106/USGS_1_n43w106_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w107/USGS_1_n43w107_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w108/USGS_1_n43w108_20230314.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w109/USGS_1_n43w109_20220805.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w110/USGS_1_n43w110_20220805.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w111/USGS_1_n43w111_20220805.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w112/USGS_1_n43w112_20240130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w115/USGS_1_n43w115_20231227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w117/USGS_1_n43w117_20231227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w118/USGS_1_n43w118_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w119/USGS_1_n43w119_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w120/USGS_1_n43w120_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w121/USGS_1_n43w121_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w122/USGS_1_n43w122_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w123/USGS_1_n43w123_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w124/USGS_1_n43w124_20210623.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w069/USGS_1_n44w069_20230302.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w070/USGS_1_n44w070_20230302.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w071/USGS_1_n44w071_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w072/USGS_1_n44w072_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w075/USGS_1_n44w075_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w076/USGS_1_n44w076_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w077/USGS_1_n44w077_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w078/USGS_1_n44w078_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w079/USGS_1_n44w079_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w080/USGS_1_n44w080_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w088/USGS_1_n44w088_20240604.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w089/USGS_1_n44w089_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w090/USGS_1_n44w090_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w091/USGS_1_n44w091_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w092/USGS_1_n44w092_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w093/USGS_1_n44w093_20240118.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w094/USGS_1_n44w094_20240118.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w095/USGS_1_n44w095_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w096/USGS_1_n44w096_20230215.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w097/USGS_1_n44w097_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w098/USGS_1_n44w098_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w099/USGS_1_n44w099_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w100/USGS_1_n44w100_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w101/USGS_1_n44w101_20220726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w102/USGS_1_n44w102_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w103/USGS_1_n44w103_20220726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w104/USGS_1_n44w104_20220726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w105/USGS_1_n44w105_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w106/USGS_1_n44w106_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w107/USGS_1_n44w107_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w108/USGS_1_n44w108_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w109/USGS_1_n44w109_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w110/USGS_1_n44w110_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w111/USGS_1_n44w111_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w112/USGS_1_n44w112_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w119/USGS_1_n44w119_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w120/USGS_1_n44w120_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w121/USGS_1_n44w121_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w122/USGS_1_n44w122_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w123/USGS_1_n44w123_20231102.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w067/USGS_1_n45w067_20230302.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w068/USGS_1_n45w068_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w069/USGS_1_n45w069_20230302.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w070/USGS_1_n45w070_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w071/USGS_1_n45w071_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w072/USGS_1_n45w072_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w075/USGS_1_n45w075_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w076/USGS_1_n45w076_20230227.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w084/USGS_1_n45w084_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w085/USGS_1_n45w085_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w086/USGS_1_n45w086_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w088/USGS_1_n45w088_20240604.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w089/USGS_1_n45w089_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w090/USGS_1_n45w090_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w091/USGS_1_n45w091_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w092/USGS_1_n45w092_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w093/USGS_1_n45w093_20240806.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w094/USGS_1_n45w094_20240806.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w095/USGS_1_n45w095_20240814.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w096/USGS_1_n45w096_20240814.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w097/USGS_1_n45w097_20240814.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w098/USGS_1_n45w098_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w099/USGS_1_n45w099_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w100/USGS_1_n45w100_20240209.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w101/USGS_1_n45w101_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w102/USGS_1_n45w102_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w103/USGS_1_n45w103_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w104/USGS_1_n45w104_20220726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w105/USGS_1_n45w105_20220726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w106/USGS_1_n45w106_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w107/USGS_1_n45w107_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w108/USGS_1_n45w108_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w109/USGS_1_n45w109_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w110/USGS_1_n45w110_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w111/USGS_1_n45w111_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w112/USGS_1_n45w112_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w116/USGS_1_n45w116_20220309.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w117/USGS_1_n45w117_20230202.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w118/USGS_1_n45w118_20230202.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w119/USGS_1_n45w119_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w120/USGS_1_n45w120_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w121/USGS_1_n45w121_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w122/USGS_1_n45w122_20220426.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w123/USGS_1_n45w123_20220426.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w124/USGS_1_n45w124_20220426.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w068/USGS_1_n46w068_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w069/USGS_1_n46w069_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w070/USGS_1_n46w070_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w071/USGS_1_n46w071_20210611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w084/USGS_1_n46w084_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w085/USGS_1_n46w085_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w086/USGS_1_n46w086_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w087/USGS_1_n46w087_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w088/USGS_1_n46w088_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w089/USGS_1_n46w089_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w090/USGS_1_n46w090_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w091/USGS_1_n46w091_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w092/USGS_1_n46w092_20240125.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w093/USGS_1_n46w093_20240806.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w094/USGS_1_n46w094_20240806.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w095/USGS_1_n46w095_20240814.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w096/USGS_1_n46w096_20240814.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w097/USGS_1_n46w097_20240814.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w098/USGS_1_n46w098_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w099/USGS_1_n46w099_20220415.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w101/USGS_1_n46w101_20230602.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w102/USGS_1_n46w102_20230614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w103/USGS_1_n46w103_20230614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w104/USGS_1_n46w104_20230614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w105/USGS_1_n46w105_20230614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w106/USGS_1_n46w106_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w107/USGS_1_n46w107_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w108/USGS_1_n46w108_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w109/USGS_1_n46w109_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w110/USGS_1_n46w110_20240325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w111/USGS_1_n46w111_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w112/USGS_1_n46w112_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w114/USGS_1_n46w114_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w115/USGS_1_n46w115_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w116/USGS_1_n46w116_20220309.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w117/USGS_1_n46w117_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w118/USGS_1_n46w118_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w119/USGS_1_n46w119_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w120/USGS_1_n46w120_20240416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w121/USGS_1_n46w121_20221128.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w122/USGS_1_n46w122_20211129.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w123/USGS_1_n46w123_20240124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w124/USGS_1_n46w124_20240124.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w068/USGS_1_n47w068_20240207.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w069/USGS_1_n47w069_20210611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w070/USGS_1_n47w070_20210611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w071/USGS_1_n47w071_20210611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w084/USGS_1_n47w084_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w085/USGS_1_n47w085_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w086/USGS_1_n47w086_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w087/USGS_1_n47w087_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w088/USGS_1_n47w088_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w089/USGS_1_n47w089_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w090/USGS_1_n47w090_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w091/USGS_1_n47w091_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w092/USGS_1_n47w092_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w093/USGS_1_n47w093_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w094/USGS_1_n47w094_20240806.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w095/USGS_1_n47w095_20240806.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w096/USGS_1_n47w096_20240329.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w097/USGS_1_n47w097_20230301.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w102/USGS_1_n47w102_20230614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w103/USGS_1_n47w103_20230614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w104/USGS_1_n47w104_20230614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w105/USGS_1_n47w105_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w106/USGS_1_n47w106_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w107/USGS_1_n47w107_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w108/USGS_1_n47w108_20210607.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w110/USGS_1_n47w110_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w111/USGS_1_n47w111_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w112/USGS_1_n47w112_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w114/USGS_1_n47w114_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w115/USGS_1_n47w115_20230119.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w117/USGS_1_n47w117_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w118/USGS_1_n47w118_20240401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w119/USGS_1_n47w119_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w120/USGS_1_n47w120_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w121/USGS_1_n47w121_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w122/USGS_1_n47w122_20220919.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w123/USGS_1_n47w123_20230608.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w124/USGS_1_n47w124_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w125/USGS_1_n47w125_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w068/USGS_1_n48w068_20210611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w069/USGS_1_n48w069_20210611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w070/USGS_1_n48w070_20210611.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w088/USGS_1_n48w088_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w089/USGS_1_n48w089_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w090/USGS_1_n48w090_20240205.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w091/USGS_1_n48w091_20240625.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w092/USGS_1_n48w092_20230326.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w093/USGS_1_n48w093_20230326.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w094/USGS_1_n48w094_20240329.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w095/USGS_1_n48w095_20240329.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w096/USGS_1_n48w096_20240329.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w097/USGS_1_n48w097_20230301.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w101/USGS_1_n48w101_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w102/USGS_1_n48w102_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w103/USGS_1_n48w103_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w104/USGS_1_n48w104_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w105/USGS_1_n48w105_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w106/USGS_1_n48w106_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w107/USGS_1_n48w107_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w109/USGS_1_n48w109_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w110/USGS_1_n48w110_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w111/USGS_1_n48w111_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w112/USGS_1_n48w112_20210607.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w114/USGS_1_n48w114_20210607.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w115/USGS_1_n48w115_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w116/USGS_1_n48w116_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w117/USGS_1_n48w117_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w118/USGS_1_n48w118_20220817.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w119/USGS_1_n48w119_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w120/USGS_1_n48w120_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w121/USGS_1_n48w121_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w122/USGS_1_n48w122_20230307.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w123/USGS_1_n48w123_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w124/USGS_1_n48w124_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w125/USGS_1_n48w125_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w090/USGS_1_n49w090_20230326.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w091/USGS_1_n49w091_20230326.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w092/USGS_1_n49w092_20230326.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w093/USGS_1_n49w093_20230326.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w094/USGS_1_n49w094_20230326.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w095/USGS_1_n49w095_20240329.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w096/USGS_1_n49w096_20240329.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w101/USGS_1_n49w101_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w102/USGS_1_n49w102_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w103/USGS_1_n49w103_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w105/USGS_1_n49w105_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w106/USGS_1_n49w106_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w107/USGS_1_n49w107_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w108/USGS_1_n49w108_20210607.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w109/USGS_1_n49w109_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w110/USGS_1_n49w110_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w111/USGS_1_n49w111_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w112/USGS_1_n49w112_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w113/USGS_1_n49w113_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w114/USGS_1_n49w114_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w115/USGS_1_n49w115_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w116/USGS_1_n49w116_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w117/USGS_1_n49w117_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w118/USGS_1_n49w118_20220817.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w119/USGS_1_n49w119_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w120/USGS_1_n49w120_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w121/USGS_1_n49w121_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w122/USGS_1_n49w122_20230307.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w123/USGS_1_n49w123_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w124/USGS_1_n49w124_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w125/USGS_1_n49w125_20240327.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w095/USGS_1_n50w095_20230326.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w096/USGS_1_n50w096_20230326.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w101/USGS_1_n50w101_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w102/USGS_1_n50w102_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w103/USGS_1_n50w103_20240723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w105/USGS_1_n50w105_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w106/USGS_1_n50w106_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w107/USGS_1_n50w107_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w108/USGS_1_n50w108_20210607.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w109/USGS_1_n50w109_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w110/USGS_1_n50w110_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w111/USGS_1_n50w111_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w112/USGS_1_n50w112_20231101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w113/USGS_1_n50w113_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w114/USGS_1_n50w114_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w115/USGS_1_n50w115_20240507.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w117/USGS_1_n50w117_20220817.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w119/USGS_1_n50w119_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w120/USGS_1_n50w120_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w121/USGS_1_n50w121_20240617.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w098/USGS_1_n26w098_20191025.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w099/USGS_1_n26w099_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w100/USGS_1_n26w100_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w101/USGS_1_n26w101_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w102/USGS_1_n26w102_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w103/USGS_1_n26w103_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w104/USGS_1_n26w104_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w105/USGS_1_n26w105_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w106/USGS_1_n26w106_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w107/USGS_1_n26w107_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w108/USGS_1_n26w108_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w109/USGS_1_n26w109_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w110/USGS_1_n26w110_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w111/USGS_1_n26w111_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w112/USGS_1_n26w112_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n26w113/USGS_1_n26w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w098/USGS_1_n27w098_20191025.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w100/USGS_1_n27w100_20190802.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w101/USGS_1_n27w101_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w102/USGS_1_n27w102_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w103/USGS_1_n27w103_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w104/USGS_1_n27w104_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w105/USGS_1_n27w105_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w106/USGS_1_n27w106_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w107/USGS_1_n27w107_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w108/USGS_1_n27w108_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w109/USGS_1_n27w109_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w110/USGS_1_n27w110_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w112/USGS_1_n27w112_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w113/USGS_1_n27w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n27w114/USGS_1_n27w114_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w097/USGS_1_n28w097_20190730.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w098/USGS_1_n28w098_20190730.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w101/USGS_1_n28w101_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w102/USGS_1_n28w102_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w103/USGS_1_n28w103_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w104/USGS_1_n28w104_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w105/USGS_1_n28w105_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w106/USGS_1_n28w106_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w107/USGS_1_n28w107_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w108/USGS_1_n28w108_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w109/USGS_1_n28w109_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w110/USGS_1_n28w110_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w111/USGS_1_n28w111_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w112/USGS_1_n28w112_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w113/USGS_1_n28w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w114/USGS_1_n28w114_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w115/USGS_1_n28w115_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n28w116/USGS_1_n28w116_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w102/USGS_1_n29w102_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w103/USGS_1_n29w103_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w105/USGS_1_n29w105_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w106/USGS_1_n29w106_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w107/USGS_1_n29w107_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w108/USGS_1_n29w108_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w109/USGS_1_n29w109_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w110/USGS_1_n29w110_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w111/USGS_1_n29w111_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w112/USGS_1_n29w112_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w113/USGS_1_n29w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w114/USGS_1_n29w114_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n29w115/USGS_1_n29w115_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w089/USGS_1_n30w089_20191212.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w106/USGS_1_n30w106_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w107/USGS_1_n30w107_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w108/USGS_1_n30w108_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w109/USGS_1_n30w109_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w110/USGS_1_n30w110_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w111/USGS_1_n30w111_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w112/USGS_1_n30w112_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w113/USGS_1_n30w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w114/USGS_1_n30w114_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w115/USGS_1_n30w115_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n30w116/USGS_1_n30w116_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w107/USGS_1_n31w107_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w108/USGS_1_n31w108_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w109/USGS_1_n31w109_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w110/USGS_1_n31w110_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w111/USGS_1_n31w111_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w112/USGS_1_n31w112_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w113/USGS_1_n31w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w114/USGS_1_n31w114_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w115/USGS_1_n31w115_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w116/USGS_1_n31w116_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n31w117/USGS_1_n31w117_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w101/USGS_1_n32w101_20191029.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w115/USGS_1_n32w115_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w116/USGS_1_n32w116_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n32w117/USGS_1_n32w117_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w100/USGS_1_n33w100_20191025.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w101/USGS_1_n33w101_20191031.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w102/USGS_1_n33w102_20191211.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w118/USGS_1_n33w118_20180313.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n33w119/USGS_1_n33w119_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w078/USGS_1_n34w078_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w079/USGS_1_n34w079_20190913.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w096/USGS_1_n34w096_20191126.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w100/USGS_1_n34w100_20191104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w101/USGS_1_n34w101_20191104.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w102/USGS_1_n34w102_20200214.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w103/USGS_1_n34w103_20200214.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w118/USGS_1_n34w118_20190917.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w119/USGS_1_n34w119_20190917.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w120/USGS_1_n34w120_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n34w121/USGS_1_n34w121_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w076/USGS_1_n35w076_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w077/USGS_1_n35w077_20151130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w078/USGS_1_n35w078_20151130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w079/USGS_1_n35w079_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w093/USGS_1_n35w093_20180814.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w094/USGS_1_n35w094_20180814.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w095/USGS_1_n35w095_20190711.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w096/USGS_1_n35w096_20190711.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w097/USGS_1_n35w097_20191125.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w098/USGS_1_n35w098_20191125.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w099/USGS_1_n35w099_20191125.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w100/USGS_1_n35w100_20191125.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w101/USGS_1_n35w101_20190923.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w102/USGS_1_n35w102_20190916.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n35w103/USGS_1_n35w103_20190916.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w076/USGS_1_n36w076_20160315.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w077/USGS_1_n36w077_20160315.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w078/USGS_1_n36w078_20151125.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w079/USGS_1_n36w079_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w092/USGS_1_n36w092_20180508.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w093/USGS_1_n36w093_20180726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w094/USGS_1_n36w094_20180726.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w095/USGS_1_n36w095_20190405.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w096/USGS_1_n36w096_20190405.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w097/USGS_1_n36w097_20190510.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w099/USGS_1_n36w099_20181010.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w100/USGS_1_n36w100_20190924.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w101/USGS_1_n36w101_20190924.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w102/USGS_1_n36w102_20190916.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n36w103/USGS_1_n36w103_20190916.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w076/USGS_1_n37w076_20151106.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w084/USGS_1_n37w084_20181127.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w085/USGS_1_n37w085_20171101.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w086/USGS_1_n37w086_20190716.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w098/USGS_1_n37w098_20181130.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w117/USGS_1_n37w117_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n37w118/USGS_1_n37w118_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w116/USGS_1_n38w116_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w117/USGS_1_n38w117_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n38w124/USGS_1_n38w124_20200115.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w116/USGS_1_n39w116_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w117/USGS_1_n39w117_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w124/USGS_1_n39w124_20200115.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w084/USGS_1_n40w084_20200302.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w109/USGS_1_n40w109_20180328.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w116/USGS_1_n40w116_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w117/USGS_1_n40w117_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n40w125/USGS_1_n40w125_20200121.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n41w073/USGS_1_n41w073_20151214.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n42w125/USGS_1_n42w125_20200122.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w082/USGS_1_n43w082_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w083/USGS_1_n43w083_20190401.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w084/USGS_1_n43w084_20190412.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w086/USGS_1_n43w086_20191107.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w087/USGS_1_n43w087_20190308.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w113/USGS_1_n43w113_20190723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w114/USGS_1_n43w114_20190723.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w116/USGS_1_n43w116_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n43w125/USGS_1_n43w125_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w066/USGS_1_n44w066_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w067/USGS_1_n44w067_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w073/USGS_1_n44w073_20181204.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w074/USGS_1_n44w074_20190416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w081/USGS_1_n44w081_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w082/USGS_1_n44w082_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w083/USGS_1_n44w083_20190409.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w084/USGS_1_n44w084_20190919.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w085/USGS_1_n44w085_20190920.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w086/USGS_1_n44w086_20190716.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w087/USGS_1_n44w087_20190308.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w113/USGS_1_n44w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w114/USGS_1_n44w114_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w115/USGS_1_n44w115_20190614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w116/USGS_1_n44w116_20190614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w117/USGS_1_n44w117_20190614.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w118/USGS_1_n44w118_20170417.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w124/USGS_1_n44w124_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n44w125/USGS_1_n44w125_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w066/USGS_1_n45w066_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w073/USGS_1_n45w073_20181204.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w074/USGS_1_n45w074_20190416.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w077/USGS_1_n45w077_20170123.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w078/USGS_1_n45w078_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w079/USGS_1_n45w079_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w080/USGS_1_n45w080_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w081/USGS_1_n45w081_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w082/USGS_1_n45w082_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w083/USGS_1_n45w083_20190325.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w087/USGS_1_n45w087_20191025.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w113/USGS_1_n45w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w114/USGS_1_n45w114_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w115/USGS_1_n45w115_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n45w125/USGS_1_n45w125_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w066/USGS_1_n46w066_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w067/USGS_1_n46w067_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w072/USGS_1_n46w072_20190506.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w073/USGS_1_n46w073_20181204.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w074/USGS_1_n46w074_20181204.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w075/USGS_1_n46w075_20180322.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w076/USGS_1_n46w076_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w077/USGS_1_n46w077_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w078/USGS_1_n46w078_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w079/USGS_1_n46w079_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w080/USGS_1_n46w080_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w081/USGS_1_n46w081_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w082/USGS_1_n46w082_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w083/USGS_1_n46w083_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w100/USGS_1_n46w100_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w113/USGS_1_n46w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n46w125/USGS_1_n46w125_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w066/USGS_1_n47w066_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w067/USGS_1_n47w067_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w072/USGS_1_n47w072_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w073/USGS_1_n47w073_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w074/USGS_1_n47w074_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w075/USGS_1_n47w075_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w076/USGS_1_n47w076_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w077/USGS_1_n47w077_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w078/USGS_1_n47w078_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w079/USGS_1_n47w079_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w080/USGS_1_n47w080_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w081/USGS_1_n47w081_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w082/USGS_1_n47w082_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w083/USGS_1_n47w083_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w098/USGS_1_n47w098_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w099/USGS_1_n47w099_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w100/USGS_1_n47w100_20160711.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w101/USGS_1_n47w101_20160711.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w109/USGS_1_n47w109_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w113/USGS_1_n47w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n47w116/USGS_1_n47w116_20190918.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w066/USGS_1_n48w066_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w067/USGS_1_n48w067_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w071/USGS_1_n48w071_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w072/USGS_1_n48w072_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w073/USGS_1_n48w073_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w074/USGS_1_n48w074_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w075/USGS_1_n48w075_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w076/USGS_1_n48w076_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w077/USGS_1_n48w077_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w078/USGS_1_n48w078_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w079/USGS_1_n48w079_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w080/USGS_1_n48w080_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w081/USGS_1_n48w081_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w082/USGS_1_n48w082_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w083/USGS_1_n48w083_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w084/USGS_1_n48w084_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w085/USGS_1_n48w085_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w086/USGS_1_n48w086_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w087/USGS_1_n48w087_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w098/USGS_1_n48w098_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w099/USGS_1_n48w099_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w100/USGS_1_n48w100_20160711.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w108/USGS_1_n48w108_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n48w113/USGS_1_n48w113_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w066/USGS_1_n49w066_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w067/USGS_1_n49w067_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w068/USGS_1_n49w068_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w069/USGS_1_n49w069_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w070/USGS_1_n49w070_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w071/USGS_1_n49w071_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w072/USGS_1_n49w072_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w073/USGS_1_n49w073_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w074/USGS_1_n49w074_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w075/USGS_1_n49w075_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w076/USGS_1_n49w076_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w077/USGS_1_n49w077_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w078/USGS_1_n49w078_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w079/USGS_1_n49w079_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w080/USGS_1_n49w080_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w081/USGS_1_n49w081_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w082/USGS_1_n49w082_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w083/USGS_1_n49w083_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w084/USGS_1_n49w084_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w085/USGS_1_n49w085_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w086/USGS_1_n49w086_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w087/USGS_1_n49w087_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w088/USGS_1_n49w088_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w089/USGS_1_n49w089_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w097/USGS_1_n49w097_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w098/USGS_1_n49w098_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w099/USGS_1_n49w099_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w100/USGS_1_n49w100_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w104/USGS_1_n49w104_20170315.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n49w126/USGS_1_n49w126_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w066/USGS_1_n50w066_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w067/USGS_1_n50w067_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w068/USGS_1_n50w068_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w069/USGS_1_n50w069_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w070/USGS_1_n50w070_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w071/USGS_1_n50w071_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w072/USGS_1_n50w072_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w073/USGS_1_n50w073_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w074/USGS_1_n50w074_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w075/USGS_1_n50w075_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w076/USGS_1_n50w076_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w077/USGS_1_n50w077_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w078/USGS_1_n50w078_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w079/USGS_1_n50w079_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w080/USGS_1_n50w080_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w081/USGS_1_n50w081_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w082/USGS_1_n50w082_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w083/USGS_1_n50w083_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w084/USGS_1_n50w084_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w085/USGS_1_n50w085_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w086/USGS_1_n50w086_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w087/USGS_1_n50w087_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w088/USGS_1_n50w088_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w089/USGS_1_n50w089_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w090/USGS_1_n50w090_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w091/USGS_1_n50w091_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w092/USGS_1_n50w092_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w093/USGS_1_n50w093_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w094/USGS_1_n50w094_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w097/USGS_1_n50w097_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w098/USGS_1_n50w098_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w099/USGS_1_n50w099_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w100/USGS_1_n50w100_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w104/USGS_1_n50w104_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w116/USGS_1_n50w116_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w118/USGS_1_n50w118_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w122/USGS_1_n50w122_20180202.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w123/USGS_1_n50w123_20180202.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w124/USGS_1_n50w124_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w125/USGS_1_n50w125_20130911.tif

https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n50w126/USGS_1_n50w126_20130911.tif



#### Reprojecting 

via [[#Better projections]])



##### New reprojection

Downloading latest 2023 landcover data, here's how QGIS wants to reproject it

```zsh

gdalwarp -overwrite -s_srs "PROJCRS["""AEA WGS84""",BASEGEOGCRS["""WGS 84""",DATUM["""World Geodetic System 1984""",ELLIPSOID["""WGS 84""",6378137,298.257223563,LENGTHUNIT["""metre""",1]]],PRIMEM["""Greenwich""",0,ANGLEUNIT["""degree""",0.0174532925199433]],ID["""EPSG""",4326]],CONVERSION["""Albers Equal Area""",METHOD["""Albers Equal Area""",ID["""EPSG""",9822]],PARAMETER["""Latitude of false origin""",23,ANGLEUNIT["""degree""",0.0174532925199433],ID["""EPSG""",8821]],PARAMETER["""Longitude of false origin""",-96,ANGLEUNIT["""degree""",0.0174532925199433],ID["""EPSG""",8822]],PARAMETER["""Latitude of 1st standard parallel""",29.5,ANGLEUNIT["""degree""",0.0174532925199433],ID["""EPSG""",8823]],PARAMETER["""Latitude of 2nd standard parallel""",45.5,ANGLEUNIT["""degree""",0.0174532925199433],ID["""EPSG""",8824]],PARAMETER["""Easting at false origin""",0,LENGTHUNIT["""metre""",1],ID["""EPSG""",8826]],PARAMETER["""Northing at false origin""",0,LENGTHUNIT["""metre""",1],ID["""EPSG""",8827]]],CS[Cartesian,2],AXIS["""easting""",east,ORDER[1],LENGTHUNIT["""metre""",1,ID["""EPSG""",9001]]],AXIS["""northing""",north,ORDER[2],LENGTHUNIT["""metre""",1,ID["""EPSG""",9001]]]]" -t_srs EPSG:5070 -r mode -of GTiff /Users/geoffrey/Downloads/Landcover2023/test_061625_nlcddata/Annual_NLCD_LndCov_2023_CU_C1V0.tif /private/var/folders/c_/lbf0gfvd56l_826nb5nf7zcm0000gn/T/processing_oUIcBI/b806358834ed486985b73f16c01df028/OUTPUT.tif

```

##### Original reprojections

```zsh

gdalwarp -overwrite -s_srs EPSG:4269 -t_srs EPSG:5070 -r average -of GTiff ./USGS_1.vrt ./USGS_1_EPSG_5070.tif



gdalwarp -overwrite -s_srs 'PROJCRS["Albers_Conical_Equal_Area",BASEGEOGCRS["WGS 84",DATUM["World Geodetic System 1984",ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],ID["EPSG",4326]],CONVERSION["unnamed",METHOD["Albers Equal Area",ID["EPSG",9822]],PARAMETER["Latitude of false origin",23,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8821]],PARAMETER["Longitude of false origin",-96,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8822]],PARAMETER["Latitude of 1st standard parallel",29.5,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8823]],PARAMETER["Latitude of 2nd standard parallel",45.5,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8824]],PARAMETER["Easting at false origin",0,LENGTHUNIT["meters",1],ID["EPSG",8826]],PARAMETER["Northing at false origin",0,LENGTHUNIT["meters",1],ID["EPSG",8827]]],CS[Cartesian,2],AXIS["easting",east,ORDER[1],LENGTHUNIT["meters",1]],AXIS["northing",north,ORDER[2],LENGTHUNIT["meters",1]]]' -t_srs EPSG:5070 -r mode -of GTiff "./Annual_NLCD_LndCov_2023_CU_C1V0.tif" "./Annual_NLCD_LndCov_2023_CU_C1V0_EPSG_5070.tif"

```

Get this command and run it in QGIS vis `Raster->Warp(Reproject)`
