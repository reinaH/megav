#superficial testing file. bc testing is important. could test so much here
# but due to the disapearing nature of the app/maps i couldnt do as much as i wanted here. 
import requests
import random
import json
from app import GoalMap, Polyanet, Soloon, Cometh


candidateId = '4bc4ea3e-ec07-4b92-8112-5aed3e422f92'
soloon_ops = ['blue', 'red', 'purple','white']
cometh_ops = ['up', 'down', 'left', 'right']

def test_goal_map():
    goal = GoalMap().goalmap

    response = requests.request("GET", GoalMap.goal_endpoint, headers=GoalMap.headers, data=GoalMap.payload)
    if (response.status_code == 500):
        assert(goal == [[]])
    elif (response.status_code == 200): 
        assert (goal == response.json()['goal'])

def test_create_polyanet():
    # for testing. since both phases were NxN's not larger than n=30
    rand = random.randrange(31)
    p = Polyanet((rand, rand)) 

    payload = json.dumps({
            "candidateId": candidateId,
            "row": rand,
            "column": rand
        })
    assert (p.payload == payload)

def test_create_soloon():
    # for testing. since both phases were NxN's not larger than n=30
    rand = random.randrange(31)
    color = random.choice(soloon_ops)
    s = Soloon((rand, rand), color=color) 

    payload = json.dumps({
            "candidateId": candidateId,
            "row": rand,
            "column": rand,
            "color": color, 
        })
    assert (s.payload == payload)

def test_create_cometh():
    # for testing. since both phases were NxN's not larger than n=30
    rand = random.randrange(31)
    direction = random.choice(cometh_ops)
    c = Cometh((rand, rand), direction=direction) 

    payload = json.dumps({
            "candidateId": candidateId,
            "row": rand,
            "column": rand,
            "direction": direction, 
        })
    assert (c.payload == payload)