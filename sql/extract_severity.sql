SELECT sev.IDpol, ClaimNb, Exposure, Area, VehPower, VehAge, DrivAge, BonusMalus, VehBrand, VehGas, Density, Region, ClaimAmount
FROM fre_mtpl2_severity AS sev
JOIN fre_mtpl2_frequency AS freq
    ON sev.IDpol = freq.IDpol