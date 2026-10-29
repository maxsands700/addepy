# AddePy

Unofficial Addepar Python SDK. Python 3.10+.

```bash
pip install addepy
# Optional DataFrame inputs:
pip install 'addepy[dataframe]'
```

Copy [`.env.example`](.env.example) to `.env`, supply credentials, and Git-ignore
that file. Select the environment provisioned for your firm.

```python
from addepy import AddePy

with AddePy.from_dotenv(".env") as client:
    entities = client.ownership.entities.list_entities(limit=10)
```

For a portfolio export, load existing query JSON copied from Addepar:

```python
from pathlib import Path
from addepy import AddePy

query = Path("portfolio-query.json").read_text(encoding="utf-8")
with AddePy.from_dotenv(".env") as client:
    with client.portfolio.jobs.execute_job(query) as response:
        result = response.json()
```

Transaction exports use `client.portfolio.transaction_jobs.execute_job(query)`.
Keep query files private. Save the job ID before waiting when resumption is needed.

[SDK documentation](docs/README.md) covers configuration, request/return shapes,
job workflows, and every wrapped endpoint. [Development](docs/development.md)
covers offline checks and explicit live diagnostics. Release notes:
[CHANGELOG.md](CHANGELOG.md).
