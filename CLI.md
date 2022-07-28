# Command Line Utility

`staratlas` command line is included in the staratlaspy package

```
$ staratlas --help
Usage: staratlas [OPTIONS] COMMAND [ARGS]...

  Main cli group

Options:
  --help  Show this message and exit.

Commands:
  score-fleet     Get score fleet info
  score-supplies  Get score supplies state
```

### Get state of supplies

```bash
$ staratlas score-supplies Fhk6AqtLT15iziGpGGrtuuvMBjHAsMykTrSAJLidCqZc
```
Output:
```
+----------------------+-----+-------+-------+-------+-------+-------------+
| Ship                 | Qty |  Fuel |  Food |  Ammo |  Tool | Resupply in |
+----------------------+-----+-------+-------+-------+-------+-------------+
| VZUS opod            |   1 | 82.8% | 49.4% | 91.5% | 84.3% | 2d 10h      |
| Pearce X5            |   6 | 56.3% | 33.0% | 78.3% | 68.6% | 16h 37m     |
| Opal Jetjet          |   3 | 22.3% |  8.0% | 67.7% | 14.9% | 17h 17s     |
| Pearce X6            |   2 | 59.6% | 35.3% | 80.3% | 71.4% | 1d 14h      |
| Rainbow Chi          |   1 | 76.6% | 36.9% | 78.1% | 71.0% | 1d 16h      |
| Fimbul BYOS Earp     |   1 | 55.6% | 39.5% | 74.4% | 75.6% | 1d 19h      |
| Calico Guardian      |   1 | 85.0% | 69.8% | 86.7% | 85.2% | 5d 40m      |
| Rainbow Om           |   1 | 88.8% | 42.3% | 84.6% | 77.9% | 1d 23h      |
| Fimbul BYOS Packlite |   3 | 72.7% | 45.1% | 83.0% | 83.6% | 2d 3h       |
| Calico Compakt Hero  |   1 | 78.2% | 54.0% | 86.2% | 77.9% | 2d 19h      |
| Pearce X4            |   6 | 86.2% | 79.0% | 93.2% | 90.0% | 19h 47m     |
| Opal Jet             |  10 | 89.1% | 78.1% | 93.5% | 88.1% | 18h 44m     |
| Tufa Feist           |   1 | 55.6% | 68.1% | 77.6% | 70.5% | 2d 23h      |
| Fimbul Airbike       |   6 | 88.4% | 76.0% | 93.2% | 88.4% | 16h 39m     |
| Ogrika Mik           |   2 | 59.6% | 38.2% | 79.3% | 73.1% | 1d 17h      |
+----------------------+-----+-------+-------+-------+-------+-------------+
```

### Get fleet info

```bash
$ staratlas score-fleet Fhk6AqtLT15iziGpGGrtuuvMBjHAsMykTrSAJLidCqZc
```
Output
```
+----------------------+-----+---------------+------------+-----------+
| Ship                 | Qty | Daily Rewards | Daily Burn | Net Yield |
+----------------------+-----+---------------+------------+-----------+
| VZUS opod            |   1 |         69.51 |      13.96 |     55.56 |
| Pearce X5            |   6 |         37.52 |       9.43 |     28.09 |
| Opal Jetjet          |   3 |         36.73 |       5.84 |     30.89 |
| Pearce X6            |   2 |         77.12 |      15.13 |     62.00 |
| Rainbow Chi          |   1 |         40.12 |       6.95 |     33.17 |
| Fimbul BYOS Earp     |   1 |         36.99 |       7.16 |     29.83 |
| Calico Guardian      |   1 |      1,174.47 |     145.03 |  1,029.44 |
| Rainbow Om           |   1 |        111.64 |      18.55 |     93.09 |
| Fimbul BYOS Packlite |   3 |        416.83 |      65.51 |    351.31 |
| Calico Compakt Hero  |   1 |        146.87 |      20.65 |    126.22 |
| Pearce X4            |   6 |          5.80 |       1.27 |      4.53 |
| Opal Jet             |  10 |          8.51 |       1.85 |      6.67 |
| Tufa Feist           |   1 |         33.95 |       7.45 |     26.50 |
| Fimbul Airbike       |   6 |          4.41 |       1.11 |      3.30 |
| Ogrika Mik           |   2 |         66.37 |      15.04 |     51.33 |
+----------------------+-----+---------------+------------+-----------+
```
By default the value is displayed in ATLAS

#### score-fleet options

```bash
$ staratlas score-fleet --help
```

```
Usage: staratlas score-fleet [OPTIONS] WALLET

  Get score fleet info

Options:
  -c, --currency [ATLAS|USDC]  Currency, either ATLAS or USDC  [default:
                               ATLAS]
  --help                       Show this message and exit.

```