# renice-win-py

Change the priority of Windows processes by executable name.

## Install

Install the `renice` command with [uv](https://docs.astral.sh/uv/):

```powershell
uv tool install .
```

To install directly from a Git checkout instead, pass its repository URL to
`uv tool install`.

## Usage

```text
renice PROCESS_NAME {real,high,above,normal,below,idle}
```

For example:

```powershell
renice chrome.exe below
```

Every process whose executable name (or first command-line argument) matches
`PROCESS_NAME` is assigned the requested Windows priority class.
