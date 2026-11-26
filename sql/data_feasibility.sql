SELECT COUNT(*) AS n_null_freq
FROM fre_mtpl2_frequency
WHERE IDpol IS NULL
   OR ClaimNb IS NULL
   OR Exposure IS NULL
   OR Area IS NULL
   OR VehPower IS NULL
   OR VehAge IS NULL
   OR DrivAge IS NULL
   OR BonusMalus IS NULL
   OR VehBrand IS NULL
   OR VehGas IS NULL
   OR Density IS NULL
   OR Region IS NULL;

SELECT COUNT(*) AS n_null_sev
FROM fre_mtpl2_severity
WHERE IDpol IS NULL
    OR ClaimAmount IS NULL;

SELECT IDpol, COUNT(*)
FROM fre_mtpl2_frequency
GROUP BY IDpol
HAVING COUNT(*) > 1;

SELECT COUNT(*) AS n_Exposure_non_positive
FROM fre_mtpl2_frequency
WHERE Exposure <=0;

SELECT COUNT(*) AS n_ClaimNb_negative
FROM fre_mtpl2_frequency
WHERE ClaimNb < 0;

SELECT COUNT(*) AS n_ClaimAmount_non_positive
FROM fre_mtpl2_severity
WHERE ClaimAmount <=0;

SELECT COUNT(*) AS n_sev_id_notin_freq
FROM fre_mtpl2_severity as sev
LEFT JOIN fre_mtpl2_frequency as freq
    ON sev.IDpol = freq.IDpol
WHERE freq.IDpol IS NULL;

SELECT COUNT(DISTINCT sev.IDpol) AS n_unique_sev_id_notin_freq
FROM fre_mtpl2_severity as sev
LEFT JOIN fre_mtpl2_frequency as freq
    ON sev.IDpol = freq.IDpol
WHERE freq.IDpol IS NULL;

WITH sev_claim_count AS (
    SELECT IDpol, COUNT(*) AS sev_claim_count
    FROM fre_mtpl2_severity
    GROUP BY IDpol
)

SELECT
    CASE
        WHEN COALESCE(sev.sev_claim_count, 0) < freq.ClaimNb THEN 'fewer'
        WHEN COALESCE(sev.sev_claim_count, 0) > freq.ClaimNb THEN 'more'
        ELSE 'match'
    END
    AS comparison,
    COUNT(*) AS n_policies
FROM fre_mtpl2_frequency AS freq
LEFT JOIN sev_claim_count AS sev
    ON freq.IDpol = sev.IDpol
GROUP BY comparison;

SELECT COUNT(*) AS n_policies_with_claims_but_no_severity
FROM fre_mtpl2_frequency AS freq
LEFT JOIN fre_mtpl2_severity AS sev
    ON freq.IDpol = sev.IDpol
WHERE freq.ClaimNb>0
    AND sev.IDpol IS NULL;

SELECT SUM(ClaimNB) AS total_reported_claims, SUM(Exposure) AS total_exposure_years, SUM(ClaimNB)/SUM(Exposure) AS claims_per_year
FROM fre_mtpl2_frequency;

SELECT COUNT(*) AS n_exposure_over_1year
FROM fre_mtpl2_frequency
WHERE Exposure>1;

SELECT MAX(Exposure) AS max_exposure
FROM fre_mtpl2_frequency;

