## how to run

 -create python virtual env:
 `python3 -m venv [name]`
 -activate venv:
`source [name]/bin/activate`
- install deps
`pip install -r requirements.txt`
- run main script that solves whatever "current" phase youre in
`python app.py`


## my notes/comments:


### note1: 
challenge is designed to only return the current phase and does not allow you to move forward and ahead. we will not divide this out into different phase solutions. this affects design in that we just grab the current solution we need bc we assume all phases reasonably are part of the same problem and build off eachother. 

### note2: 
this solution is scalable. unless `limit_per_host=1` were noted the defualt is about 100 open connections at once. another solution to limiting and timing the resources is with a semaphone. in theory this could be scaled to hit millions of links in a reasonable span of time.

i did not experiment too much on what an ideal limit is but while debugging i did find that if you place no limit the megaverse api does not like it and not all requests get processed appropriately despite logging that says that all calls were made and returned 200's. this issue was actually where i spent the most time on- i did not understand why the map was not displaying properly despite it processing all tasks and returning appropriate response codes, only after a while did i realize pacing the requests was the solution and not the async code. initially i thought that some part of the async code was causing the loop to leave tasks unfinished but the task counters reflected otherwise. 

### note3:
http bodies are case sensitive and if i tried to create an object w upper v lower case parameters (ex: BLUE vs blue) the map would render a question mark emoji at that index. i wanted to note that i noticed this but did not really have an opportunity to account for it as it was at the bottom of the todo list and then the map disapeared from view. 

## if i could add improvements to app:

backend: i think what could make this assignment better is to add a 'currentmegaverse' endpoint. it would be nice to be able to just validate the current megaverse against the solution endpoint without having to physically look at it. that and risk the map 'disappearing'- if you do have the right solution as soon as you 'validate' you risk losing the current view. 


testing: i would do a lot more with regards to testing. i added very simple test cases bc no program is complete without a test suite but theres so more that can be done.   




