<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!--Based on "Description of Bathymetric Attributed Grid Object (BAG) Version 1.5.1"-->
<schema xmlns="http://purl.oclc.org/dsdl/schematron" schemaVersion="iso">
    <!-- Namespaces required for the validation -->
    <ns uri="http://www.isotc211.org/2005/gmi" prefix="gmi"/>
    <ns uri="http://www.isotc211.org/2005/gmd" prefix="gmd"/>
    <ns uri="http://www.isotc211.org/2005/gco" prefix="gco"/>
    <ns uri="http://www.opennavsurf.org/schema/bag" prefix="bag"/>
    <!-- Phase definitions for make possible step-wise validation -->
    <phase id="phase.generic_checks">
        <active pattern="generic_checks"/>
    </phase>
    <phase id="phase.MI_Metadata_checks">
        <active pattern="MI_Metadata_checks"/>
        <active pattern="MI_Metadata_checks_2"/>
        <active pattern="MI_Metadata_checks_3"/>
        <active pattern="MI_Metadata_language_checks"/>
        <active pattern="MI_Metadata_dateStamp_checks"/>
        <active pattern="MI_Metadata_name_checks"/>
        <active pattern="MI_Metadata_version_checks"/>
    </phase>
    <phase id="phase.gmd_indentificationInfo">
        <active pattern="gmd_indentificationInfo_checks"/>
    </phase>
    <phase id="phase.gmd_dataQualityInfo">
        <active pattern="gmd_dataQualityInfo_checks"/>
    </phase>
    <phase id="phase.gmd_spatialRepresentationInfo">
        <active pattern="gmd_spatialRepresentationInfo_checks"/>
    </phase>
    <phase id="phase.gmd_EX_GeographicBoundingBox">
        <active pattern="gmd_EX_GeographicBoundingBox_west_east_checks"/>
        <active pattern="gmd_EX_GeographicBoundingBox_south_north_checks"/>
    </phase>
    <!-- Generic checks -->
    <pattern id="generic_checks">
        <title>Generic checks</title>
        <rule context="/">
            <assert test="gmi:MI_Metadata | gmd:MD_Metadata">
                The document root must be an gmi:MI_Metadata or an gmd:MD_Metadata element.
            </assert>
        </rule>
    </pattern>
    <!-- gmi:MI_Metadata-level checks -->
    <pattern id="MI_Metadata_checks">
        <rule context="/gmi:MI_Metadata | gmd:MD_Metadata">
            <assert test="gmd:metadataConstraints/gmd:MD_LegalConstraints">
                The gmi:MI_Metadata element must have a gmd:metadataConstraints/gmd:MD_LegalConstraints [$5.3.1.1].
            </assert>
        </rule>
    </pattern>
    <pattern id="MI_Metadata_checks_2">
        <rule context="/gmi:MI_Metadata | gmd:MD_Metadata">
            <assert test="gmd:metadataConstraints/gmd:MD_SecurityConstraints">
                The gmi:MI_Metadata element must have a gmd:metadataConstraints/gmd:MD_SecurityConstraints [$5.3.1.1].
            </assert>
        </rule>
    </pattern>
    <pattern id="MI_Metadata_checks_3">
        <rule context="/gmi:MI_Metadata | gmd:MD_Metadata">
            <assert test="count(gmd:referenceSystemInfo) = 2">
                The gmi:MI_Metadata element must have a gmd:referenceSystemInfo for horizontal datum and
                gmd:referenceSystemInfo for vertical datum [$5.3.1.1].
            </assert>
        </rule>
    </pattern>
    <pattern id="MI_Metadata_language_checks">
        <rule context="/gmi:MI_Metadata/gmd:language | gmd:MD_Metadata/gmd:language">
            <assert test="count(.)">
                The BAG XML Metadata Library requires this node [$5.3.1.7].
            </assert>
        </rule>
        <rule context="/gmi:MI_Metadata/gmd:language/gmd:LanguageCode | gmd:MD_Metadata/gmd:language/gmd:LanguageCode">
            <assert test="normalize-space(@codeListValue) = 'en' or normalize-space(@codeListValue) = 'eng'">
                The gmd:languageCode value must be 'en' (iso639-1) or 'eng' (iso639-2) [$5.3.1.1].
            </assert>
        </rule>
    </pattern>
    <pattern id="MI_Metadata_dateStamp_checks">
        <rule context="/gmi:MI_Metadata/gmd:dateStamp | gmd:MD_Metadata/gmd:dateStamp">
            <assert test="count(child::gco:Date) = 1">
                The BAG XML Metadata Library requires this node [$5.3.1.9].
            </assert>
        </rule>
    </pattern>
    <pattern id="MI_Metadata_name_checks">
        <rule context="/gmi:MI_Metadata/gmd:metadataStandardName | gmd:MD_Metadata/gmd:metadataStandardName">
            <assert test="count(.) = 1">
                The BAG XML Metadata Library requires this node [$5.3.1.10].
            </assert>
        </rule>
        <rule context="/gmi:MI_Metadata/gmd:metadataStandardName/gco:CharacterString | gmd:MD_Metadata/gmd:metadataStandardName/gco:CharacterString">
            <assert test="normalize-space(.) = 'ISO 19139' or normalize-space(.) = 'ISO 19115'">
                The gmd:metadataStandardName/gco:CharacterString value must be 'ISO 19139' or '19115' [$5.3.1.1].
            </assert>
        </rule>
    </pattern>
    <pattern id="MI_Metadata_version_checks">
        <rule context="/gmi:MI_Metadata/gmd:metadataStandardVersion | gmd:MD_Metadata/gmd:metadataStandardVersion">
            <assert test="count(.) = 1">
                The BAG XML Metadata Library requires this node [$5.3.1.11].
            </assert>
        </rule>
    </pattern>
    <!-- gmi:MI_Metadata/gmd:identificationInfo-level checks -->
    <pattern id="gmd_indentificationInfo_checks">
        <rule context="/gmi:MI_Metadata/gmd:identificationInfo/bag:BAG_DataIdentification | gmd:MD_Metadata/gmd:identificationInfo/bag:BAG_DataIdentification">
            <assert test="count(.) >= 1">
                The gmd:identificationInfo/bag:BAG_DataIdentification must exist [$5.3.1.2].
            </assert>
            <assert test="child::gmd:language/gmd:LanguageCode[@codeListValue = 'en'] or child::gmd:language/gmd:LanguageCode[@codeListValue = 'eng']">
                The gmd:languageCode value must be 'en' (iso639-1) or 'eng' (iso639-2) [$5.3.1.1].
            </assert>
            <assert test="child::gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode[@codeListValue = 'grid']">
                The gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode should be set to 'grid' [$5.3.1.2].
            </assert>
            <assert test="normalize-space(child::gmd:topicCategory/gmd:MD_TopicCategoryCode) = 'elevation'">
                The gmd:topicCategory/gmd:MD_TopicCategoryCode should be set to 'elevation' [$5.3.1.2].
            </assert>
            <assert test="count(child::bag:verticalUncertaintyType) >= 1">
                The bag:verticalUncertaintyType must exist [$5.3.1.2].
            </assert>
        </rule>
    </pattern>
    <!-- gmi:MI_Metadata/gmd:dataQualityInfo-level checks -->
    <pattern id="gmd_dataQualityInfo_checks">
        <rule context="/gmi:MI_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality | gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality">
            <assert test="child::gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode[@codeListValue = 'dataset']">
                The gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode is always set to 'dataset' [$5.3.1.4].
            </assert>
        </rule>
        <rule context="/gmi:MI_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage
        | gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage">
            <assert test="(count(child::gmd:processStep) > 0) or (count(child::gmd:source) > 0)">
                The gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage must have at least 1 source and/or at least 1 processStep [$5.3.1.4].
            </assert>
        </rule>
    </pattern>
    <!-- gmi:MI_Metadata/gmd:spatialRepresentationInfo-level checks -->
    <pattern id="gmd_spatialRepresentationInfo_checks">
        <rule context="/gmi:MI_Metadata/gmd:spatialRepresentationInfo/gmd:MD_Georectified | gmd:MD_Metadata/gmd:spatialRepresentationInfo/gmd:MD_Georectified">
            <assert test="child::gmd:numberOfDimensions >= 2">
                The gmd:MD_Georectified/gmd:numberOfDimensions must specify at least two dimensions [$5.3.1.5].
            </assert>
            <assert test="child::gmd:numberOfDimensions = count(child::gmd:axisDimensionProperties)">
                The number of gmd:axisDimensionProperties must correspond to gmd:MD_Georectified/gmd:numberOfDimensions [$5.3.1.5], but <value-of select="normalize-space(child::gmd:MD_Georectified/gmd:numberOfDimensions)"/>!=<value-of select="normalize-space(count(child::gmd:MD_Georectified/gmd:axisDimensionProperties))"/>.
            </assert>
        </rule>
    </pattern>
    <!-- gmd:EX_GeographicBoundingBox-level checks -->
    <pattern id="gmd_EX_GeographicBoundingBox_west_east_checks">
        <rule context="/gmi:MI_Metadata/gmd:identificationInfo/bag:BAG_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox">
            <assert test="child::gmd:eastBoundLongitude >= child::gmd:westBoundLongitude">
                The eastern longitude (<value-of select="normalize-space(child::gmd:eastBoundLongitude)"/>) must be greater than the western longitude (<value-of select="normalize-space(child::gmd:westBoundLongitude)"/>).
            </assert>
        </rule>
    </pattern>
    <pattern id="gmd_EX_GeographicBoundingBox_south_north_checks">
        <rule context="/gmi:MI_Metadata/gmd:identificationInfo/bag:BAG_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox">
            <assert test="child::gmd:northBoundLatitude >= child::gmd:southBoundLatitude">
                The northern latitude (<value-of select="normalize-space(child::gmd:northBoundLatitude)"/>) must be greater than the southern latitude (<value-of select="normalize-space(child::gmd:southBoundLatitude)"/>).
            </assert>
        </rule>
    </pattern>
</schema>
