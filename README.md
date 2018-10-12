## Minimal Interview Scheduler Project.

## Installation (Unix & Mac only)
Execute following commands on your favorite terminal application.

#### Clone the packages
```git clone git@github.com:sardok/is-1.git && cd is-1```


#### Create virtualenv for application
```virtualenv venv --python=python3```


#### Install dependencies
```source venv/bin/activate && pip install -r requirements.txt```

#### Run tests (optional)
``` pytest tests ```

#### Run the application
``` flask run ```

## Demonstration

One may find script & data for demo purpose under `test-scenario` directory.

Example:

```
$ cd test-scenario && sh play.sh
Interviewer Sarah's schedule is added (for WW41 & 42).                                                                                                                                                                                                                                    
Interviewer Philip's schedule is added (for WW 41 42).                                                                                                                                                                                                                                    
Candidate Carl's schedule is added (for WW 41 & 42).                                                                                                                                                                                                                                      
Fetching results for Carl as candidate, Philip and Sarah as interviewers.                                                                                                                                                                                                                 
[                                                                                                                                                                                                                                                                                         
    {                                                                                                                                                                                                                                                                                     
        "begin": "Tue, 16 Oct 2018 09:00:00 GMT",                                                                                                                                                                                                                                         
        "end": "Tue, 16 Oct 2018 10:00:00 GMT",                                                                                                                                                                                                                                           
        "name": "Philip",                                                                                                                                                                                                                                                                 
        "type": "Interviewer"                                                                                                                                                                                                                                                             
    },                                                                                                                                                                                                                                                                                    
    {                                                                                                                                                                                                                                                                                     
        "begin": "Tue, 16 Oct 2018 09:00:00 GMT",                                                                                                                                                                                                                                         
        "end": "Tue, 16 Oct 2018 10:00:00 GMT",                                                                                                                                                                                                                                           
        "name": "Sarah",                                                                                                                                                                                                                                                                  
        "type": "Interviewer"                                                                                                                                                                                                                                                             
    },                                                                                                                                                                                                                                                                                    
    {                                                                                                                                                                                                                                                                                     
        "begin": "Tue, 16 Oct 2018 09:00:00 GMT",                                                                                                                                                                                                                                         
        "end": "Tue, 16 Oct 2018 10:00:00 GMT",                                                                                                                                                                                                                                           
        "name": "Carl",                                                                                                                                                                                                                                                                   
        "type": "Candidate"                                                                                                                                                                                                                                                               
    },                                                                                                                                                                                                                                                                                    
    {                                                                                                                                                                                                                                                                                     
        "begin": "Thu, 18 Oct 2018 09:00:00 GMT",                                                                                                                                                                                                                                         
        "end": "Thu, 18 Oct 2018 10:00:00 GMT",                                                                                                                                                                                                                                           
        "name": "Philip",                                                                                                                                                                                                                                                                 
        "type": "Interviewer"                                                                                                                                                                                                                                                             
    },
    {
        "begin": "Thu, 18 Oct 2018 09:00:00 GMT",
        "end": "Thu, 18 Oct 2018 10:00:00 GMT",
        "name": "Sarah",
        "type": "Interviewer"
    },
    {
        "begin": "Thu, 18 Oct 2018 09:00:00 GMT",
        "end": "Thu, 18 Oct 2018 10:00:00 GMT",
        "name": "Carl",
        "type": "Candidate"
    }
]
```

## Api

#### Schedule

The given data strcuture should be given as

```
{
  "name": "Name of Person",
  "schedules": [
    ["Begin datetime (EU format)", "End datetime (EU format)"],
    .
    .
    .
  ]
}
```

Concrete example:
```
{
  "name": "Carl",
  "schedules": [
    ["10.10.2018 10:00", "10.10.2018 12:00"],

    ["15.10.2018 9:00", "15.10.2018 10:00"],
    ["16.10.2018 9:00", "16.10.2018 10:00"],
    ["17.10.2018 9:00", "17.10.2018 10:00"],
    ["18.10.2018 9:00", "18.10.2018 10:00"],
    ["19.10.2018 9:00", "19.10.2018 10:00"]
  ]
}
```


#### Scheduling

Assuming application is running on `localhost:5000`.

##### Interviewer

`curl http://localhost:5000/schedule/interviewer -d @data.json -H 'content-type: application/json'`


##### Candidate

`curl http://localhost:5000/schedule/candidate -d @data.json -H 'content-type: application/json'`

#### Retrieving Schedules

The returning data structure as a result of following api calls are in following format

```
[                                                                                                                                                                                                                                                                                         
    {                                                                                                                                                                                                                                                                                     
        "begin": "Scheduled Interview Begin Datetime",                                                                                                                                                                                                                                         
        "end": "Scheduled Interview End Datetime",                                                                                                                                                                                                                                           
        "name": "Name of the interviewer or candidate",                                                                                                                                                                                                                                                                 
        "type": "Interviewer OR Candidate"                                                                                                                                                                                                                                                             
    },
    .
    .
]
```

Concrete Example

```
[                                                                                                                                                                                                                                                                                         
    {                                                                                                                                                                                                                                                                                     
        "begin": "Tue, 16 Oct 2018 09:00:00 GMT",                                                                                                                                                                                                                                         
        "end": "Tue, 16 Oct 2018 10:00:00 GMT",                                                                                                                                                                                                                                           
        "name": "Philip",                                                                                                                                                                                                                                                                 
        "type": "Interviewer"                                                                                                                                                                                                                                                             
    }
]
```

##### Querying Schedules

`curl http://localhost:5000/schedule/query?candidate=Candidate1&candidate=Candidate2&interviewer=Interviewer1&interviewer=Interviewer2 ...`

The returning result should give the schedules matching for all given candidate(s) and interviewer(s).

One may want to see best scheduled times among candidates or interviewers only.

###### Get the intersected schedules for candidates John & Mary.

`curl http://localhost:5000/schedule/query?candidate=John&candidat=Mary`

###### Get the intersected schedules for interviewers Mark and Jax.

`curl http://localhost:5000/schedule/query?interviewer=Mark&interviewer=Jax`

##### Retrieve all interviewers' schedules

`curl http://localhost:5000/schedule/query/interviewers`

##### Retrieve all candidates' schedules

`curl http://localhost:5000/schedule/query/candidates`

##### Retrieve all schedules

`curl http://localhost:5000/schedule/all`



