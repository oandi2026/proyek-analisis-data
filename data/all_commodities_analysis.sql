
SELECT sl.State AS nama_negara_bagian, SUM(yp.Value) AS total_yogurt
FROM yogurt_production yp
JOIN state_lookup sl ON yp.State_ANSI = sl.State_ANSI
GROUP BY sl.State
ORDER BY total_yogurt DESC
LIMIT 5;




