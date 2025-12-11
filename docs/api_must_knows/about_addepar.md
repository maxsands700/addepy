# Addepar 101

## About Addepar

Addepar is a wealth management platform specializing in data aggregation, flexible analysis, and dynamic reporting for even the most complex portfolios. Additionally, Addepar connects to the other tools you use to run your business.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/825be6b-Overview.png",
"Overview.png",
1647
],
"align": "center",
"sizing": "80"
}
]
}
[/block]

Addepar gathers portfolio and market data, such as dividend and interest payments,\
into a single place, letting you see all this information side by side.

Addepar works with partners like Fidelity, Schwab, and other custodians for portfolio data as well as with leading market data providers and other providers for market data.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/c7aa920-Data_Aggregation.png",
"Data Aggregation.png",
1580
],
"align": "center",
"sizing": "80"
}
]
}
[/block]

Additionally, you can manually manage holdings in Addepar to see private investments, such as real estate and private equity investments, alongside publicly-traded securities.

After all portfolio data is aggregated, you can analyze it any way you wish. Whether you want to see a household’s, a client’s overall portfolio value, or the return of a particular private equity fund, you can quickly run that analysis in Addepar.

Addepar’s reporting engine lets you scale your business. Rather than creating and re-creating reports for each client, you can create a report once then enable it for any portfolio you want.

Dynamic reporting features let you flip between portfolios to see client data automatically update in the Report Editor.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/9547fda-Dynamic_Reporting.png",
"Dynamic Reporting.png",
1580
],
"align": "center",
"sizing": "80"
}
]
}
[/block]

When communicating with your clients, you can choose to download reports as PDF files, share reports through the online client portal, and give your clients on-the-go insight into their holdings via Addepar Mobile.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/d6b6ebd-Client_Communications.png",
"Client Communications.png",
1647
],
"align": "center",
"sizing": "80"
}
]
}
[/block]

In addition to its core aggregation, analysis, and reporting functionality, Addepar integrates with the other systems you use every day.

Addepar’s integrations with trading and rebalancing platforms, customer relationship management tools, and other applications let you automate workflows and increase operational efficiency.

Additionally, you can use the Addepar API to tailor a custom solution to fit your firm’s needs.

## Ownership Structure

In Addepar, a portfolio is any collection of assets that you want to organize together for analysis and reporting purposes. Households, clients, legal entities, accounts, and groups are all considered portfolios. Please note that household entity type was released in 2024 and is not reflected on the following figures. More information about the new household entity type is available on Addepar Help Center and can be provided upon request.

Portfolios in Addepar are based on an ownership structure and described by attributes. An ownership structure is a hierarchy of households, clients, legal entities, accounts, and investments.

Group portfolios are a collection of household, client, legal entity, or account portfolios. Selecting a portfolio lets you access all of its information across the various tabs.

It’s important to note that regardless of how an ownership structure is formatted, you have the flexibility to view it from different perspectives without having to restructure it. For example, let’s say you have a client that owns two trusts. Selecting the client portfolio lets you see information for all of the client’s holdings. But, you can also select one of the trusts to see only the holdings in that trust.

This flexibility is due to the ownership structure.

- Households can own all parts of the portfolio.
- Clients can own all parts of the portfolio except for households.
- Legal entities can own other legal entities, accounts, and investments.
- Accounts can own other accounts and investments.
- Investments cannot own anything themselves.

A position connects each part of the hierarchy. In Addepar, a position is a relationship between two parts of a portfolio, and it holds information like value, percent of ownership, and inception date.

An ownership structure can vary in its complexity. It’s common for a client to own a legal entity, account, or investment directly. It’s also common for a client to indirectly own an account through a legal entity. In the below graphic, the legal entity directly owns the account.

A client can also share ownership of a legal entity, account, or investment with another person. This is called joint ownership.

After a portfolio’s ownership structure is complete, you can add details to it using attributes. Learn more about attributes in the Attributes section below.

## Analysis & Transactions

**Analysis**\
All of the aggregated portfolio data (collected from custodians, market data providers, or input by the users as attributes) can be organized and examined using a multitude of features on the Analysis tab within the application.

Information in Analysis is presented in a view. Each view contains an asset table and up to two charts. The asset table consists of rows — called "groupings" — and columns. Groupings act as categories and subcategories of information in the table.

Remember that attributes are qualitative and quantitative details you can use to organize and analyze data in Addepar. All of the information you see in Analysis is a combination of portfolio and transaction attributes.

**Transactions**\
The Transactions tab within the application houses all transactions received from custodians and other data providers, as well as the ones manually added to the firm.

Each transaction includes attributes like trade date and posted date, and you can create transaction views just like you can in Analysis.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/b9b2059-Transactions.png",
"Transactions.png",
1580
],
"align": "center",
"sizing": "80"
}
]
}
[/block]

## Attributes

After a portfolio’s ownership structure is complete, you can add details to it using attributes. Attributes are qualitative and quantitative details you can use to organize and analyze data in Addepar.

For example, when you create an account, you can specify the portfolio’s asset class or region using attributes. Also, positions between parts of a portfolio have attributes.

Other attributes, such as value, percent of ownership, and inception date, can also be used in views as columns and groupings.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/21e5968-Attributes.png",
"Attributes.png",
1580
],
"align": "center",
"sizing": "80"
}
]
}
[/block]

Views and reports are used to organize and analyze the attribute values (data) in a meaningful way.

Take transactions, for example. When a transaction comes in from a data provider, Addepar attempts to parse the transaction’s data and then assign relevant attributes to each piece. For example, if the transaction includes a trade date, then the Trade Date attribute is applied to the transaction, and the date itself becomes the attribute’s value. Similarly, if the transaction includes the number of shares bought, then the Shares Bought attribute is applied, and the quantity itself becomes the attribute’s value.

Addepar may also infer that the transaction is a buy (shares purchased), so the Type attribute is applied, and “Buy” becomes the attribute’s value. So on and so forth.

If an online transaction doesn’t include certain information, or if you’re manually entering a new transaction, you can apply additional attributes to specify whatever information you choose.

Attributes can be both quantitative and qualitative. Like quantitative attributes associated with transactions, attributes can also be qualitative, such as asset class, sector, or region.

Once attributes are applied, you can create views and reports to analyze attribute values. Following the example above, you could filter by Type in Transactions, and only display buy transactions. You could then add Trade Date as a column to sort chronologically, and Shares Bought as another column to quickly scan and compare quantities.
