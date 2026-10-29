# Configuration

```python
from addepy import AddePy

with AddePy.from_dotenv(".env") as client:
    user = client.admin.users.get_current_user()
```

## Sources

| Construction | Reads |
| --- | --- |
| `AddePy.from_dotenv(path, **overrides)` | Exactly that file; relative to working directory; Git optional. |
| `AddePy.from_dotenv(**overrides)` | Nearest ancestor Git repository's root `.env`, starting at working directory. |
| `AddePy.from_env(**overrides)` | Process `ADDEPAR_*` variables. |
| `AddePy(...)` | Explicit arguments. |

Missing file/repository: `FileNotFoundError`. File loading neither merges process
values nor interpolates `${VARIABLE}` nor mutates the environment. Overrides
replace source values. Any authentication override replaces the entire source
authentication method; supply both key fields together.

## Settings

Use [`.env.example`](../.env.example). Require `firm_id` and either `firm_name`
or `base_url`. Supply exactly one authentication method.

| Constructor argument | File/process variable | Meaning/default |
| --- | --- | --- |
| `firm_id` | `ADDEPAR_FIRM_ID` | Firm header; required. |
| `firm_name` | `ADDEPAR_FIRM_NAME` | Hostname prefix. |
| `environment` | `ADDEPAR_ENVIRONMENT` | `production` (default), `sandbox`, `development`. |
| `base_url` | `ADDEPAR_BASE_URL` | Explicit HTTPS API URL including version; overrides hostname construction. |
| `key_id`, `key_secret` | `ADDEPAR_KEY_ID`, `ADDEPAR_KEY_SECRET` | Raw Basic key pair; SDK encodes it. |
| `api_key` | `ADDEPAR_API_KEY` | Base64 `key_id:key_secret`; optional `Basic ` prefix. |
| `access_token` | `ADDEPAR_ACCESS_TOKEN` | Bearer token; optional `Bearer ` prefix. |
| `token_provider` | — | Callable returning an access token; alternative authentication. |
| `timeout` | — | `(10, 60)` seconds: connect/read; positive scalar also accepted. |
| `max_retries`, `max_retry_wait` | — | `2` retries, maximum delay `60` seconds. |
| `session`, `download_session` | — | Optional Requests sessions; caller owns injected sessions. |

Constructed URLs end in `/api/v1`: production `{firm_name}.addepar.com`, sandbox
`{firm_name}.sandbox.addepar.com`, development `{firm_name}.clientdev.addepar.com`.
Use `base_url="https://api.addepar.com/v1"` for an explicitly configured global host.

```python
client = AddePy.from_dotenv(".env", timeout=(10, 90), max_retries=0)
client.close()
```

## OAuth refresh

Register/authorize the application separately. `OAuthTokenProvider` posts a
refresh grant to the supplied `token_url`, uses returned `expires_in`, and calls
`on_token_update(tokens)` after refresh so the application can persist rotation.

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

These `OAUTH_*` names belong to the example; factories read only the table's
`ADDEPAR_*` names. Provider options: `access_token=None`, `expires_in=0`,
`timeout=30`, `session=None`, `on_token_update=None`. Calling the provider or
`get_token(deadline=None)` returns a token; the optional deadline is monotonic.
`close()`/context exit closes only its owned session.

Implementation: [client.py](../addepy/client.py),
[configuration.py](../addepy/configuration.py), [auth.py](../addepy/auth.py).
