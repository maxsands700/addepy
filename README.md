# AddePy

Unofficial Python SDK for Addepar. Python 3.10+.

## Install

```bash
pip install addepy
```

## Configure

Create a `.env` file in your project directory with your Addepar API credentials:

```dotenv
ADDEPAR_ENVIRONMENT=production
ADDEPAR_FIRM_NAME=yourfirm
ADDEPAR_FIRM_ID=12345
ADDEPAR_KEY_ID=your_key_id
ADDEPAR_KEY_SECRET=your_key_secret
```

Add `.env` to your project's `.gitignore`. Use `sandbox` or `development` if that is the environment provisioned for your firm.

```python
from addepy import AddePy

with AddePy.from_dotenv(".env") as client:
    entities = client.ownership.entities.list_entities(limit=10)
```

The path is relative to your working directory. `AddePy.from_dotenv()` without a path reads the nearest Git repository's root `.env`. Encoded API keys, OAuth, and process environment variables are also supported; see [configuration](docs/configuration.md).

## Portfolio query job

Save query JSON copied from Addepar as `portfolio-query.json`, then run:

```python
from pathlib import Path
from addepy import AddePy

query = Path("portfolio-query.json").read_text(encoding="utf-8")

with AddePy.from_dotenv(".env") as client:
    result = client.portfolio.jobs.execute_job(query).json()
```

## Transaction query job

Save your transaction query as `transaction-query.json`:

```python
from pathlib import Path
from addepy import AddePy

query = Path("transaction-query.json").read_text(encoding="utf-8")

with AddePy.from_dotenv(".env") as client:
    result = client.portfolio.transaction_jobs.execute_job(query).json()
```

Both methods submit once, wait for completion, and download the result. They accept JSON text or a dictionary containing query parameters, either directly or under `data.attributes`. Keep query files private. For saved views, large exports, or resuming a job after a timeout, see [jobs](docs/jobs.md).

## Documentation
- [Configuration](docs/configuration.md): credentials, environments, timeouts, and retries.
- [Jobs](docs/jobs.md): query inputs, downloads, and resumption.
- [Resources](docs/resources.md): pagination, imports, and other APIs.
- [Development](docs/development.md): tests, live diagnostics, and packaging.
- [Changelog](CHANGELOG.md).
