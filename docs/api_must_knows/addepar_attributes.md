# Addepar Attributes

Attributes are qualitative and quantitative details that you can use to organize and analyze data in Addepar. Addepar comes with over 300 Standard Attributes and allows for creating Custom Attributes to record and calculate data that is not covered.

The Entities API, Positions API, and Groups API can be used to characterize entities, positions, and groups beyond their required resource attributes. All attributes are grouped under the "attributes" object of the resource. The exception is market data attributes, which cannot be retrieved.

> 👍
>
> [The Attributes API](https://developers.addepar.com/docs/attributes) can be used to discover attributes available for use in the Portfolio Query, Entities, and Positions APIs.
>
> Attributes and their respective API field name can also be found in the application. Open Addepar, navigate to the Global Navigation bar and click on Firm Administration.
>
> Select Attributes on the left menu under Data Configuration, and then select the attribute from the list to display its details, including its API Field Name.
> [block:parameters]
> {
> "data": {

    "h-0": "",
    "h-1": "Description",
    "h-2": "Example",
    "0-0": "Standard Attributes",
    "0-1": "Built-in attributes provided by Addepar.  \n  \nThese include descriptive details about portfolio owners and investments.",
    "0-2": "Display Name:  `Asset Class`  \n  \nAPI Field Name: `asset_class `",
    "1-0": "Custom Attributes",
    "1-1": "Custom attributes are identified in the API with the prefix \"_custom_\" (to easily differentiate between standard and custom attributes), followed by the attribute's given name, and finally its Addepar attribute ID (to differentiate it from other, similarly-named custom attributes).",
    "1-2": "Display Name: `GIC Taxonomy`  \n  \nAPI Field Name: `_custom_gic_taxonomy_637951`",
    "2-0": "External Partner Identifiers",
    "2-1": "External IDs are attributes that connect identifiers (External ID Types) across Addepar and non-Addepar systems and applications.  \n  \nExternal IDs use the prefix “external_id” followed by the “external_type_key” in the API.  \n  \nSupported for entities and groups only.  \n  \nRead the [Setup Guide](https://developers.addepar.com/v2.187.0/docs/external-identifiers-beta) for External IDs.",
    "2-2": "Display Name: `Salesforce`  \n  \nAPI Field Name:  \n  \n`external_id_salesforce`"

},
"cols": 3,
"rows": 3,
"align": [
"left",
"left",
"left"
]
}
[/block]

**Standard Attribute Example**

Applying the above standard attribute "Asset Class" to an entity.

```json Example
{
  "data": {
    "id": "207",
    "type": "entities",
    "attributes": {
      "asset_class": "Equity"
    }
  }
}
```

**Custom Attribute Example**

Applying the above custom attribute "GIC Taxonomy" to a position.

```json Example
{
  "data": {
    "id": "61580665",
    "type": "positions",
    "attributes": {
      "_custom_gic_taxonomy_637951": [
        {
          "value": "Emerging Market"
        }
      ]
    }
  }
}
```

**_External ID Attribute Example_**

Applying the above external ID "Salesforce" to an entity.

```json Example
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

> 📘 Date formatting in responses
>
> Display names for certain columns, attributes, and entities will match your firm's date formatting in successful responses. The options for date formatting are presently month-day-year or day-month-year.

\*\*Output Types\
\*\*\
Both standard and custom attributes can hold any of the below Addepar output types. See the "Usage" section of [Attributes API](https://developers.addepar.com/docs/attributes) to learn more about attribute applicability:

| Output Type | Description                              | Example                                |
| :---------- | :--------------------------------------- | :------------------------------------- |
| Word        | A string.                                | `"Equities"`                           |
| Number      | A number.                                | `100`                                  |
| Percentage  | A percentage expressed as a decimal.     | `0.05`                                 |
| Date        | A date in YYYY-MM-DD format.             | `"2017-03-30"`                         |
| Yes/No      | A boolean (true or false).               | `true`                                 |
| Currency    | Currency code as a string                | `"USD"`                                |
| Money Value | An object containing currency and value. | `{"currency": "USD", "value": 167.23}` |

**Time-Varying Attributes**

Some Addepar Attributes and all Custom Attributes can support time-varying outputs to reflect changes in the attribute's value over time (for example, to record a change in a stock's geography by holding different values before or after a merger or another event).

All time-varying attributes have three required fields: `date`, `value`, and `weight`. Each field must be present, regardless of whether the field's value is null or non-null.

When the value of `date` is null, it means the value and `weight` apply at all points in time. When multiple dates are included for an attribute, it means the values of `value` and `weight` apply as of that `date`.

The value of `weight` must be a decimal. Non-decimals will cause an error. For example, using `1.0` instead of `1`.

Some attributes can have multiple values on the same date. To represent this, `weight` takes on a decimal value or value less than one. For example, if a stock is listed in two sectors on the same date, and the stock is divided between the two sectors 50/50, the value of each sector's weight is `0.5`.

The example below shows the different ways a time-varying attribute may appear.

```json Example
"attributes":{
  "asset_class":[
    {
      "date":null,
      "value":"Equity",
      "weight":1.0
    }
  ],
  "country":[
    {
      "date":"2015-01-01",
      "value":"USA",
      "weight":1.0
    },
    {
      "date":"2018-01-01",
      "value":"2018-01-01",
      "weight":1.0
    }
  ],
  "sector":[
    {
      "date":"2018-01-01",
      "value":"CAD",
      "weight":1.0
    },
    {
      "date":"2018-01-01",
      "value":"Large Cap",
      "weight":0.5
    }
  ]
}
```

**Money Value Attributes**

All money value attributes have two required fields: `value` and `currency`. Both fields must be present. The example below shows how the money value Next Call Price attribute appears.

```json Example
"attributes":{
  "call_price":{
    "value":100,
    "currency":"USD"
  }
}
```
