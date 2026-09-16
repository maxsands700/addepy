# Configuration

Use a context manager to close the client's connections when finished:

```python
from addepy import AddePy

with AddePy.from_dotenv(".env") as client:
    user = client.admin.users.get_current_user()
```

## Configuration sources

| Factory | Reads |
| --- | --- |
| `AddePy.from_dotenv(".env")` | Exactly that file; relative paths start at the working directory. Works without Git. |
| `AddePy.from_dotenv()` | The nearest ancestor Git repository's root `.env`, starting at the working directory. |
| `AddePy.from_env()` | Process `ADDEPAR_*` variables only. |
| `AddePy(...)` | Explicit constructor arguments only. |

A missing file or repository raises `FileNotFoundError`. File loading does not merge process variables, expand `${VARIABLE}` references, or change the process environment. Keyword arguments override source values:

```python
client = AddePy.from_dotenv(".env", timeout=(10, 90), max_retries=0)
client.close()
```

## Credentials and environments

Start with [`.env.example`](../.env.example). Set `ADDEPAR_FIRM_ID` and either `ADDEPAR_FIRM_NAME` or a full `ADDEPAR_BASE_URL`. Choose exactly one authentication method:

| File/process variables | Constructor arguments | Meaning |
| --- | --- | --- |
| `ADDEPAR_KEY_ID` and `ADDEPAR_KEY_SECRET` | `key_id`, `key_secret` | Raw Basic key pair; SDK performs base64 encoding. |
| `ADDEPAR_API_KEY` | `api_key` | Already base64-encoded `key_id:key_secret`, optionally prefixed with `Basic `. |
| `ADDEPAR_ACCESS_TOKEN` | `access_token` | OAuth access token, optionally prefixed with `Bearer `. |

An authentication keyword override replaces the entire authentication method from the source. Supply both key fields when overriding a key pair.

`ADDEPAR_ENVIRONMENT` / `environment` defaults to `production`:

| Environment | Constructed API base URL |
| --- | --- |
| `production` | `https://{firm_name}.addepar.com/api/v1` |
| `sandbox` | `https://{firm_name}.sandbox.addepar.com/api/v1` |
| `development` | `https://{firm_name}.clientdev.addepar.com/api/v1` |

Use the environment provisioned for your firm. `ADDEPAR_BASE_URL` / `base_url` overrides hostname construction; include the API version, for example `https://yourfirm.addepar.com/api/v1`. API URLs require HTTPS.

## OAuth refresh

For automatic refresh, supply an `OAuthTokenProvider` as `token_provider=`. Register and authorize the OAuth application separately. The provider uses the token response's `expires_in` and calls `on_token_update` with refreshed tokens so your application can persist rotated refresh tokens.

```python
import os
from addepy import AddePy, OAuthTokenProvider

with OAuthTokenProvider(
    token_url=os.environ["OAUTH_TOKEN_URL"],
    client_id=os.environ["OAUTH_CLIENT_ID"],
    client_secret=os.environ["OAUTH_CLIENT_SECRET"],
    refresh_token=os.environ["OAUTH_REFRESH_TOKEN"],
) as tokens:
    with AddePy.from_env(token_provider=tokens) as client:
        user = client.admin.users.get_current_user()
```

Use your application's token endpoint for the selected environment. These `OAUTH_*` names are application settings used by the example; the SDK factories only read the `ADDEPAR_*` settings above.

## HTTP behavior

The default request timeout is `(10, 60)` seconds for connection and read respectively. Transient read failures can retry twice; set `max_retries=0` to disable retries. Writes require explicit `retry=True` on `client.request(...)` and a body that can be replayed. A server retry delay above `max_retry_wait` (default 60 seconds) raises the original error instead of retrying early.

SDK request exceptions inherit from `AddePyError` and expose `status_code`, `request_id`, `errors`, and `response` when available. HTTP error messages omit response bodies. Connection failures raise `TransportError`; request timeouts raise `RequestTimeoutError`. See [jobs](jobs.md) for polling deadlines and job failures.

Pass a `requests.Session` as `session=` to customize connections; injected sessions remain caller-owned. Cross-host download redirects strip API credentials, firm headers, and cookies. Polling deadlines also bound SDK-managed requests, retries, and OAuth refresh. Stream read timeouts limit inactivity, not total download duration.
