// Paste into Power Query Advanced Editor and name the query quarterly.
let
    Source = Csv.Document(Web.Contents("https://raw.githubusercontent.com/Krgaurav93084/Tesla-Business-KPI-Analysis/main/analytics_v2/quarterly.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"quarter_end",type date},{"revenue_usd_m",Int64.Type},{"gross_profit_usd_m",Int64.Type},{"operating_income_usd_m",Int64.Type},{"production",Int64.Type},{"deliveries",Int64.Type},{"inventory_days",Int64.Type},{"automotive_revenue_usd_m",Int64.Type},{"energy_revenue_usd_m",Int64.Type},{"services_revenue_usd_m",Int64.Type}},"en-US")
in
    Types
