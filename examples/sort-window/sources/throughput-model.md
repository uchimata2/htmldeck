# Marnfield depot — throughput model

**Marnfield is an illustrative parcel network. It does not exist.** Every figure below is an output
of the assumptions stated with it, and none of it is attributed to any real operator, study or
place.

## Volume

| | Parcels per day | Basis |
| :--- | ---: | :--- |
| October baseline | 18,400 | mean of 22 working days |
| Peak, 18 November to 23 December | 27,600 | mean of 31 working days |
| Busiest single day, 5 December | 31,900 | observed maximum |

Peak volume runs **50%** above the October baseline. The sorter, the fleet and the shift pattern do
not change with it.

## The sort

One sorter line. Rated at **3,100** parcels per hour and it holds that rate to within 4% across a
full shift, so the model treats it as constant.

Inbound arrives on two trunk services:

| Trunk | Arrives | Parcels, peak | Sort finishes |
| :--- | :--- | ---: | :--- |
| First | 19:40 | 20,400 | 00:14 |
| Second | 23:40 | 7,200 | 01:59 |

The second trunk's 7,200 parcels take **2h 19m** at 3,100 per hour. Sorting cannot start before the
trunk is unloaded, so the finish time is arrival plus sort time and nothing compresses it.

**The outbound cut-off is 01:00.** A parcel sorted after it waits a day. The second trunk therefore
clears **59 minutes** past the cut-off.

## Failure

Next-day delivery missed:

| | Missed | Basis |
| :--- | ---: | :--- |
| Off-peak | 3.1% | October, 22 working days |
| Peak | 12.4% | 18 November to 23 December |

Where the peak failures happen, sampled over 14 nights:

| | Share of misses |
| :--- | ---: |
| Still unsorted at the 01:00 cut-off | 84% |
| Sorted, not loaded before the round left | 16% |

Monthly miss rate, next-day: July 2.9%, August 3.0%, September 3.4%, October 3.1%,
November 9.8%, December 15.2%.

By district, peak:

| District | Missed | Position in the loading sequence | Depot to district centre | Rounds | First away |
| :--- | ---: | :--- | ---: | ---: | :--- |
| Ashgrove | 4.1% | first | 9 miles | 6 | 04:10 |
| Cranleigh | 11.2% | second | 14 miles | 5 | 04:35 |
| Dellow | 15.9% | third | 6 miles | 4 | 05:05 |
| Beacon Hill | 18.7% | last | 11 miles | 7 | 05:30 |

Distance does not order this column and loading position does. The worst-served district is
**11 miles** from the depot and the best-served is 9; the district 14 miles out sits third.

The sequence is stable enough to argue from. Over the 31 peak nights sampled, Ashgrove was loaded
first on every one, and Beacon Hill last on **27 of 31**.

**Excluded from every figure above:** returns, same-day services, and the two weeks either side of
the depot's August resurfacing, when volume was diverted.
