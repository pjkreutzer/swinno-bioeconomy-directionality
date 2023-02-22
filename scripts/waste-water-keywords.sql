SELECT innovation.[SINNO ID],
  use_sectors.use_sectors as sni,
  innovation.[Innovation name in Swedish],
  innovation.[Description in Swedish] as des,
  innovation.[Additional information if Origin = New scientific discovery] || innovation.[Additional information if Origin = New technologies or materials] || innovation.[Additional info if Origin = Official regulation, legislation and standards.] || innovation.[Additional information if Origin = Solution for a problem.] || innovation.[Additional information if Origin = Performance] || innovation.[Additional information if Origin = Other] AS [Additional Info]
FROM innovation
  JOIN use_sectors ON innovation.[SINNO ID] = use_sectors.[SINNO ID]
  WHERE sni LIKE '90%'
  AND (des LIKE '%skog%' OR des LIKE 'trä%' OR des LIKE '%papper%' OR des LIKE '%cellulose%')