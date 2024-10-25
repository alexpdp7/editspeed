# editspeed

editspeed measures your speed reproducing some text with your editor.

## Installation

With `pipx`:

```
pipx install git+https://github.com/alexpdp7/editspeed.git
```

## Sample usage

```
editspeed rainbow.txt --top-margin=1
```

## Run without installing

```
pipx run --spec git+https://github.com/alexpdp7/editspeed.git editspeed <(curl https://raw.githubusercontent.com/alexpdp7/editspeed/refs/heads/main/rainbow.txt)
```

## Caveats

* Only works with bash.
