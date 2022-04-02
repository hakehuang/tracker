# Introduction

ConV19 like disease infection track and simulation

# quick start

```
pip install -r requirements.txt
python ./tracker.py
```

# code structure

## disease.py
	defines a diseases including

## interface.py
	infection interfaces and paient infection diagram

## people.py
	modeling the people who will infected by certain disease

## tracker.py
	implement entry

# Assumptions

in tracker.py we assume every people will walk randomly 500 steps, which mean 500 steps will be a day, and trigger day updates

# intial data

```
_ps = cal_pos(9, 1, [20, 20], PEOPLE_SQUARE)
```
in cal_pos the initial 
9 victims
1 illness
start walking from a 20 by 20 rect
start point is PEOPLE_SQUARE
