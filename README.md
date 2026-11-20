# Supply Chain & Logistics Performance Analytics

## Project Overview
An end-to-end data analytics project focused on analyzing supply chain operations, sales performance, profitability, shipping methods, and delivery efficiency using SQL, Python, and Power BI.

The project transforms raw supply chain data into meaningful business insights through data cleaning, SQL analysis, Python visualizations, and an interactive Power BI dashboard.

## Objectives
- Analyze overall sales, revenue, profit, and order performance.
- Evaluate product categories and department-level performance.
- Understand customer segment and market contribution.
- Analyze delivery delays and shipping performance.
- Investigate the relationship between discounts and profitability.
- Identify regional differences in logistics performance.

## Tech Stack
- **Database:** PostgreSQL
- **Query Language:** SQL
- **Programming:** Python
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Psycopg2
- **Visualization:** Power BI
- **Tools:** pgAdmin 4, Power BI Desktop, VS Code

## Dataset
- Dataset: DataCo Smart Supply Chain Dataset
- Original Records: 180,519
- Original Columns: 53
- Cleaned Records: 180,519
- Cleaned Columns: 42

Data cleaning included column removal, date validation, missing-value checks, duplicate checks, and the creation of additional analytical columns.

## Project Workflow
1. Data inspection and profiling
2. Data quality investigation
3. Data cleaning and preprocessing using Python
4. Database creation and data import into PostgreSQL
5. SQL-based business analysis
6. Python-based data visualization
7. Interactive dashboard development in Power BI

## Key Business Insights

- Total Revenue: 36.78M
- Total Profit: 3.97M
- Total Orders: 65,752
- Average Order Value: 559.45
- Overall Profit Margin: 10.78%
- Late Delivery Orders: 36,048 distinct orders

### Additional Findings
- Consumer segment contributed approximately 51.91% of total revenue.
- Europe contributed approximately 29.56% of total revenue.
- First Class shipping had a 95.27% late-delivery item rate.
- Higher discount bands were associated with lower profit margins in the analyzed dataset.
- The dataset showed a structural change in average items per order from October 2017 onward, which should be considered when comparing monthly trends.

## Power BI Dashboard

The interactive dashboard contains three analytical pages:

1. **Executive Overview** – Overall business performance, KPIs, revenue trends, market and customer segment analysis.
2. **Sales & Product Analysis** – Product category performance, order status, discounts, and profitability.
3. **Supply Chain & Delivery Analysis** – Delivery status, shipping modes, shipping delays, and regional performance.

## Data Interpretation Notes
- The dataset is at order-item level. Item counts and distinct order counts are different.
- Late-delivery item rates should not be interpreted as late-delivery order rates.
- The currency unit was not independently confirmed; financial figures are therefore shown without a currency symbol.
- Observed relationships are analytical associations and do not establish causation.

## Project Outputs
- Cleaned dataset
- SQL analysis scripts
- Python analysis and visualization scripts
- Generated analytical charts
- Power BI dashboard (.pbix)
- Dashboard report (.pdf)

## Conclusion
This project demonstrates an end-to-end data analytics workflow, combining SQL, Python, and Power BI to evaluate supply chain performance and support data-driven business decisions.