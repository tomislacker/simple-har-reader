# Simple HAR Reader
This program was mostly put together as a simple proof-of-concept for a friend.

## Usage
### Installation
+ Python

### Invocation

#### Switches - General

+ `-f`/`--file` - Specify a [.har] file to be read
+ `-P`/`--no-pretty-print` - Disable pretty-print *(Default is to display pretty-printed JSON)*

#### Switches - Operations

+ `-T` - Return bytes rx/tx for one or more sessions (.har files). *(This is the default)*

### Examples
#### Read Files & Show Bytes Rx/Tx

*With pretty-print*

```sh
$ python read.py \
    -f har/sample01.har \
    --file har/sample02.har \
    -P
{'browser_tx': 49735, 'browser_rx': 3094292}
```

*Without pretty-print*

```sh
$ python read.py \
    -f har/sample01.har \
    --file har/sample02.har
{
    "browser_rx": 3094292,
    "browser_tx": 49735
}
```
