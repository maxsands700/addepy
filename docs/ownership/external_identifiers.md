# External IDs

An External ID allows you to seamlessly query portfolio data across Addepar and non-Addepar systems and applications. You can set it up in 4 steps:

1. Create External ID Types
2. Map External ID Types
3. Query Portfolio Data using External ID
4. Review the External ID in Addepar

## Step 1: Create External ID Types

External ID Types are objects representing each non-Addepar system or application. Be sure to make one type for each system you'd like to query portfolio data from. You can create an External ID Type using the External ID Types API.

**POST** `/v1/external_id_types`

```json Example
POST  https://examplefirm.addepar.com/api/v1/external_id_types

{
   "data": {
      "type": "external_id_types",
      "attributes": {
         "external_type_key": "salesforce",
         "display_name": "Salesforce"
      }
   }
}
```

## Step 2: Map External ID Types

Once you’ve made a unique type for each system, use the Entities API to map them to the appropriate system or application.

**PATCH** `/v1/entities /:entity_id`

```json Example
PATCH https://examplefirm.addepar.com/api/v1/entities/217

{
   "data": {
      "id": "217",
      "type": "entities",
      "attributes": {
         "external_id_salesforce": "MDM123"
      }
   }
}
```

## Step 3: Query Portfolio Data using an External ID

You can now request portfolio data with Portfolio Query API via the external ID.

**POST** `/v1/portfolio/query`

```json Example
POST https://examplefirm.addepar.com/api/v1/portfolio/query

{
   "data": {
      "type": "portfolio_query",
      "attributes": {
         "columns": [
            {
               "key": "value",
               "arguments": {
                  "time_point": "current",
                  "accrued": "all",
                  "valuation_adjustment_type": "none",
                  "currency": "USD"
               }
            },
            {
               "key": "node_id"
            }
         ],
         "groupings": [
            {
               "key": "asset_class"
            },
            {
               "key": "ownership"
            }
         ],
         "filters": [],
         "portfolio_type": "entity",
         "portfolio_id": [],
         "external_ids": [
            {
               "external_type_key": "salesforce",
               "external_id": "MDM123"
            }
         ],
         "start_date": "2021-06-29",
         "end_date": "2021-07-29",
         "hide_previous_holdings": false,
         "group_by_historical_values": false,
         "group_by_multiple_attribute_values": false,
         "look_through_composite_securities": false,
         "display_account_fees": false
      }
   }
}
```

## Step 4: Review the External ID in Addepar

1. Select a portfolio with an external ID mapped.
2. Click the Analysis tab.
3. In the upper right corner of the table, click the pencil icon.
4. Add a column for "External ID."
5. Select an "External ID Type."
6. Refresh the view.

![](https://files.readme.io/8400c54-External_ID_1.png "External ID (1).png")
