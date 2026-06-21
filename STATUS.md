# Status

## Current state

v0.1 is runnable as a local Python module.

Implemented:

- default TSMC Arizona capex-plan fixture
- five-factor curated scoring fixture
- deterministic JSONL report artifact
- CLI commands: `validate` and `diagnose`
- pytest coverage for fixture validation, probability closure, and deterministic report rendering

## Known limits

- Factor weights are curated fixtures.
- The output artifact is JSONL only.
- There is one firm-plan and one project.
- Backtest calibration is not implemented.

## Next feature queue

- Add schema files that mirror the current runtime validators.
- Add Markdown report rendering from the JSONL diagnostic artifact.
- Add calibration tests once a backtest fixture set exists.

- Resolve factory defect: implementation produced no file changes relative to base; refusing to mark a no-op as done
- Resolve factory defect: === reviewer: claude_code ===
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,"duration_ms":13593,"duration_api_ms":12473,"num_turns":4,"result":"API Error: Server is temporarily limiting requests (not your usage limit) · Rate limited","stop_reason":"stop_sequence","session_id":"70c1b88c-612f-4130-a859-d4e92e9f9c3a","total_cost_usd":0.1150005,"usage":{"input_tokens":8,"cache_creation_input_tokens":9572,"cache_read_input_tokens":81445,"output_tokens":558,"server_tool_u
- Resolve factory defect: missing pyproject.toml
- Resolve factory defect: STATUS.md missing required section '## Current state'
- Resolve factory defect: STATUS.md missing required section '## Known limits'
- Resolve factory defect: STATUS.md missing required section '## Next feature queue'
- Resolve factory defect: expected file 'pyproject.toml' is missing
- Resolve factory defect: expected file 'src/binding_constraint/cli.py' is missing
- Resolve factory defect: module 'cli' declares source 'src/binding_constraint/cli.py', but it is missing
- Resolve factory defect: module 'model' declares source 'src/binding_constraint/model.py', but it is missing
- Resolve factory defect: module 'report' declares source 'src/binding_constraint/report.py', but it is missing
- Resolve factory defect: === reviewer: claude_code ===
{"type":"result","subtype":"success","is_error":false,"api_error_status":null,"duration_ms":21736,"duration_api_ms":21486,"num_turns":4,"result":"STATUS: NEEDS_PATCH\nFINDINGS:\n- `pyproject.toml` is missing (contract-presence + contract:missing-expected-artifact both fail). Required by the contract — add a minimal pyproject for the `binding_constraint` package.\n- Package is at top-level `binding_constraint/` but the contract (SYSTEM_MAP module sources) expects `sr
- Resolve factory defect: expected file 'src/binding_constraint/cli.py' is missing
- Resolve factory defect: module 'cli' declares source 'src/binding_constraint/cli.py', but it is missing
- Resolve factory defect: module 'model' declares source 'src/binding_constraint/model.py', but it is missing
- Resolve factory defect: module 'report' declares source 'src/binding_constraint/report.py', but it is missing
- Resolve factory defect: === reviewer: claude_code ===
{"type":"result","subtype":"success","is_error":false,"api_error_status":null,"duration_ms":110427,"duration_api_ms":109476,"num_turns":11,"result":"STATUS: NEEDS_PATCH\n\nFINDINGS:\n- Four factory-contract gates FAIL on layout/naming mismatch: contract expects `src/binding_constraint/cli.py`, `src/binding_constraint/model.py`, `src/binding_constraint/report.py`, but the implementer placed the package at flat `binding_constraint/` (per `pyproject.toml` `packages = [
