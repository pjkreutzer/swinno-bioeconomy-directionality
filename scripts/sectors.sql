SELECT innovation.[SINNO ID],
  use_sectors.use_sectors,
  innovation.[Innovation name in Swedish],
  innovation.[Description in Swedish],
  innovation.[Additional information if Origin = New scientific discovery] || innovation.[Additional information if Origin = New technologies or materials] || innovation.[Additional info if Origin = Official regulation, legislation and standards.] || innovation.[Additional information if Origin = Solution for a problem.] || innovation.[Additional information if Origin = Performance] || innovation.[Additional information if Origin = Other] AS [Additional Info]
FROM innovation
  JOIN use_sectors ON innovation.[SINNO ID] = use_sectors.[SINNO ID]
WHERE innovation.[SINNO ID] NOT IN (
    7373001,
    13015001,
    10655001,
    10230001,
    10161001,
    10050001,
    9772001,
    9617001,
    9599001,
    9591001,
    9590001,
    9589001,
    9584001,
    9583001,
    9582001,
    9578001,
    9575001,
    9526001,
    9520001,
    9473001,
    9438001,
    8838001,
    8432001,
    8389001,
    8314001,
    8312001,
    8220001,
    8117001,
    8014001,
    8004001,
    8003001,
    7875001,
    7791001,
    7675001,
    7559001,
    7558001,
    7557001,
    7553001,
    7552001,
    7547001,
    7545001,
    7541001,
    7540001,
    7533001,
    7532001,
    7529001,
    7516001,
    7511001,
    7510001,
    7507001,
    7506001,
    7505001,
    7503001,
    7499001,
    7498001,
    7492001,
    7482001,
    7475001,
    7474001,
    7468001,
    7467001,
    7465001,
    7464001,
    7463001,
    7459001,
    7458001,
    7457001,
    7450001,
    7442001,
    7438001,
    7433001,
    7432001,
    7427001,
    7425001,
    7424001,
    7423001,
    7414001,
    7408001,
    7390001,
    7388001,
    7382001,
    7370001,
    7367001,
    7365001,
    7363001,
    7362001,
    7140001,
    6990001,
    6954001,
    6943001,
    6942001,
    6933001,
    6852001,
    6848001,
    6834001,
    6814001,
    6778001,
    6777001,
    6764001,
    6746001,
    6707001,
    6341001,
    6314001,
    6191001,
    6029001,
    6044001,
    6163001,
    6182001,
    6191001,
    6194001,
    6203001,
    6238001,
    6281001,
    6314001,
    6325001,
    6341001,
    6348001,
    6425001,
    6685001,
    6689001,
    6695001,
    6707001,
    6740001,
    6746001,
    6759001,
    6760001,
    6764001,
    6768001,
    6774001,
    6777001,
    6778001,
    6787001,
    6788001,
    6795001,
    6814001,
    6822001,
    6824001,
    6834001,
    6837001,
    6842001,
    6848001,
    6852001,
    6933001,
    6942001,
    6943001,
    6954001,
    6977001,
    6988001
  ) 
  AND (
    use_sectors.use_sectors LIKE '01%'
    OR use_sectors.use_sectors LIKE '02%'
    OR use_sectors.use_sectors LIKE '13%'
    OR use_sectors.use_sectors LIKE '16%'
    OR use_sectors.use_sectors LIKE '17%'
    OR use_sectors.use_sectors LIKE '18%'
    OR use_sectors.use_sectors LIKE '20%'
    OR use_sectors.use_sectors LIKE '38%'
    OR use_sectors.use_sectors LIKE '41%');

-- Why did I choose these sectors, they make no sense!
-- Right, because they make sense for the 2007 SNI codes.
-- But even then why would I want to look at sector 18, Grafisk produktion och reproduktion av inspelningar?
  
