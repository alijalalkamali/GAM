# Coocurrance Simulation
The Coocurrance.py script utilizes [data extracted from from news articles](https://github.com/alijalalkamali/GAM/tree/data-extraction) to simulate actions of geopolitical agents.  

An example run of the simulation:

```
> python Coocurrance.py -h

optional arguments:
  -h, --help  show this help message and exit
  --cf CF     Coocurrance File
  -a A        Number of Agents
  --ho HO     Horizon
  -v V        Verbose


> python Coocurrance.py --cf CooccuranceOutput2013.csv -a 2 --ho 3 
Creating World
Creating Agents
Creating Agent: A1
Adding Agent to World
Creating Agent: A2
Adding Agent to World
Set Weights to Prioritize States
Y to set weights. To skip, press any other key. >
... 
[Program will prompt to set weights for states]
...
Set Termination Conditions
Y to set termination conditions.  To skip, press any other key. > Y
['force', 'cooperation', 'welfare', 'military', 'tie', 'economy', 'price', 'tension', 'trade']
Select State: > economy
Set Termination State Value: > 110
Setting Termination Condition: if economy reaches value of 110
Select State: > military
Set Termination State Value: > 120
Setting Termination Condition: if military reaches value of 120
Y to set more termination conditions.  To continue, press any other key. > n
Set Reward Conditions
Y to set reward conditions.  To skip, press any other key. Y
['force', 'cooperation', 'welfare', 'military', 'tie', 'economy', 'price', 'tension', 'trade']
Select Goal State: > economy
Minimize(1), Maximize(2), or Minimize Difference(3)?: > 2
Setting Reward Condition
Y to set reward conditions.  To skip, press any other key. Y
['force', 'cooperation', 'welfare', 'military', 'tie', 'economy', 'price', 'tension', 'trade']
Select Goal State: > tension
Minimize(1), Maximize(2), or Minimize Difference(3)?: > 3
['force', 'cooperation', 'welfare', 'military', 'tie', 'economy', 'price', 'tension', 'trade']
Select State to Minimize difference with tension: > trade
Setting Reward Condition
Y to set more reward conditions.  To continue, press any other key. > n
100%
A1-accuse
100%
A2-accuse
100%
A1-join
100%
A2-allow
100%
...
```



