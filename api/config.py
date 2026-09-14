from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings


_REPO_ROOT = Path(__file__).parent.parent


class Settings(BaseSettings):
    spl_dir: Path = Path.home() / "projects/digital-duck/SPL.py"
    public_domains: Path = _REPO_ROOT / "public" / "domains"
    llm: str = "claude_cli:claude-sonnet-5"
    default_model: str = "gemma4"
    spl_while_max_iter: int = 50
    spl_max_llm_calls: int = 50

    # User-supplied API keys for adapters that need one (set from the
    # Settings page, kept in-memory only like every other setting here —
    # never echoed back to the browser, only injected into the spl3
    # subprocess env at generate time; see executor.py's _ADAPTER_ENV_VAR).
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    openai_api_key: str = ""
    openrouter_api_key: str = ""

    model_config = {"env_prefix": "CB_", "env_file": ".env", "extra": "ignore"}

    # example.env/.env.example ship CB_SPL_DIR=~/projects/digital-duck/SPL.py
    # and CB_PUBLIC_DOMAINS=./public/domains as the documented defaults —
    # pydantic's Path validator does neither "~" expansion nor relative-path
    # resolution, so a .env that sets either verbatim from the template ends
    # up with a path that's only valid when the current process happens to
    # have the repo root as its cwd. executor.py's create_subprocess_exec
    # uses spl_dir as the child's cwd and passes public_domains-derived
    # paths as a --param string to a spl3 subprocess running in yet another
    # cwd, so both silently break as soon as either differs — surfacing as
    # an uninformative uvloop "FileNotFoundError: [Errno 2] No such file or
    # directory" (spl_dir) or a ToolFailed deep inside spl3 pointing at a
    # path resolved relative to the wrong directory entirely
    # (public_domains, resolved by graph_lib.load_domain as a last resort
    # relative to its own file's directory).
    @field_validator("spl_dir", mode="before")
    @classmethod
    def _expand_spl_dir(cls, v):
        return Path(v).expanduser() if v else v

    @field_validator("public_domains", mode="before")
    @classmethod
    def _resolve_public_domains(cls, v):
        if not v:
            return v
        p = Path(v).expanduser()
        return p if p.is_absolute() else (_REPO_ROOT / p).resolve()


settings = Settings()
