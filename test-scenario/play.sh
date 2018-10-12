#!/bin/bash

curl -s http://localhost:5000/schedule/interviewer -d @sarah.json -H "content-type: application/json" > /dev/null
echo "Interviewer Sarah's schedule is added (for WW41 & 42)."

curl -s http://localhost:5000/schedule/interviewer -d @philip.json -H "content-type: application/json" > /dev/null
echo "Interviewer Philip's schedule is added (for WW 41 42)."

curl -s http://localhost:5000/schedule/candidate -d @carl.json -H "content-type: application/json" > /dev/null
echo "Candidate Carl's schedule is added (for WW 41 & 42)."

echo "Fetching results for Carl as candidate, Philip and Sarah as interviewers."
curl -s "http://localhost:5000/schedule/query?candidate=Carl&interviewer=Philip&interviewer=Sarah" | python -m json.tool
