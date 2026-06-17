## Agricultural Commodities Production Analysis (US Data)

### Executive Summary & Key Insights

This project analyzes the production data of various agricultural commodities across different US states. By leveraging SQL JOIN and aggregation techniques, several critical supply chain and agricultural insights were uncovered:

1. **Dairy Supply Chain Decoupling (Milk vs. Cheese)**
   - While states like Iowa (ANSI: 19) and Pennsylvania (ANSI: 42) lead in raw milk production, the downstream manufacturing of cheese is heavily dominated by Wisconsin (ANSI: 55) and California (ANSI: 6). 
   - *Insight:* This indicates a geographic specialization where certain states focus on upstream dairy farming, while others possess stronger industrial infrastructure for high-value food processing.

2. **Coffee Processing Hubs**
   - The analysis revealed an anomaly where non-tropical states like Wisconsin and California registered the highest volumes for coffee production. 
   - *Insight:* Since coffee plants cannot grow in these climates, this data reflects post-harvest processing industries (roasting, blending, and packaging) localized near major shipping ports and distribution hubs, rather than actual crop farming.

3. **Midwest Dominance in Egg Production**
   - Ohio (ANSI: 39) and Indiana (ANSI: 18) emerged as the top producers in egg production. 
   - *Insight:* This aligns perfectly with agricultural logistics, as the Midwest "Corn Belt" produces the massive supply of corn and soybeans required for poultry feed.

4. **Yogurt Production Concentrated Near Populated Markets**
   - New York and California strongly lead the yogurt manufacturing sector. 
   - *Insight:* Due to the shorter shelf-life and refrigeration constraints of yogurt compared to cheese, manufacturing plants are strategically located closer to massive consumer population centers.
