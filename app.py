# imports. 
import requests
import time
import aiohttp
import asyncio
import json
from aiohttp import ClientSession

# quick reference of space object options: 
# SPACE
# POLYANET
# BLUE_SOLOON
# WHITE_SOLOON
# PURPLE_SOLOON
# RED_SOLOON
# LEFT_COMETH
# RIGHT_COMETH
# UP_COMETH
# DOWN_COMETH

# in a prod env this might be more similar to key and would be stored in an env doc and not so visibly
candidateId = '4bc4ea3e-ec07-4b92-8112-5aed3e422f92'

# class definitions

class GoalMap():
    # class attrs
    goal_endpoint = '{}/api/map/{}/goal'.format(base, candidateId)
    payload={}
    headers={}

    # instance attrs
    def __init__(self):
        self.goalmap = self.get_goal_map()
        self.numrows = len(self.goalmap) #overkill but added so app doesnt break if we get a map that is not a nice NxN
        self.numcols = len(self.goalmap[0])

    # #####
    def get_goal_map(self):
        response = requests.request("GET", GoalMap.goal_endpoint, headers=GoalMap.headers, data=GoalMap.payload)

        if response.status_code == 200:
            return(response.json()['goal'])
        else: 
            return [[]] #when we get to the end this endpoint breaks so if not 200, just return empty map

class AstralObjectsMapper():
    # instance attrs
    def __init__(self, goalmap):
        self.astral_objects = self.astral_objects_mapper(goalmap, len(goalmap), len(goalmap[0]))
    
    # #####
    def astral_objects_mapper(self, goalmap, numrows, numcols):
        # this does one sweep and sorts and creates our objects to feed to our async client.
        # 
        # a very easy and 2-3 line alternative to do this would be to cast our solution array to a numpy array
        # and have the numpy array return all indicies of each object ocurrance. chose do do this 
        # because the numpy route would have in theory travered the matrix one time for every astral object
        # whereas this is one sweep
        #  
        astralobjects = []
        
        for row in range(numrows):
            for col in range(numcols):

                curr = goalmap[row][col].split('_')
                 
                if curr[0] == 'SPACE':                    
                    pass
                elif curr[0] == 'POLYANET':                    
                    currpolyanet = Polyanet((row,col))
                    astralobjects.append(currpolyanet)

                elif curr[1] == 'SOLOON':
                    currsoloon = Soloon((row,col), curr[0].lower()) #http bodies are case sensitive
                    astralobjects.append(currsoloon)

                elif curr[1] == 'COMETH':
                    currcometh = Cometh((row,col), curr[0].lower()) #http bodies are case sensitive
                    astralobjects.append(currcometh)
                            
        return (astralobjects)


# ################
class AstralObject():
    def __init__(self):
        self.base = 'https://challenge.crossmint.io'
        self.headers = {
        'Content-Type': 'application/json'
        }




class  Polyanet(AstralObject):
    # available HTTP methods:
    # POST - arguments: row and col
    # DELETE - arguments: row and col

    # class attrs
    endpoint = '/api/polyanets'

    # instance attrs
    def __init__(self, index):
        super().__init__()
        self.name='POLYANET'
        self.index=index
        self.payload = self.get_payload(index[0], index[1])
        self.url= (self.base + Polyanet.endpoint) #overkill as each instance has the same val but kept bc in theory is more scalable

    # #####
    def get_payload(self, row, column):
        payload = json.dumps({
            "candidateId": candidateId,
            "row": row,
            "column": column
        })

        return payload

class  Soloon(AstralObject):
    # available HTTP methods:
    # POST - arguments: row, col, color
    # DELETE - arguments: row, col

    # class attrs
    endpoint = '/api/soloons'

    # instance attrs
    def __init__(self, index, color):
        super().__init__()
        self.name='SOLOON'
        self.index=index
        self.payload=self.get_payload(index[0], index[1], color)
        self.color=color
        self.url= (self.base + Soloon.endpoint) #overkill as each instance has the same val but kept bc in theory is more scalable

    # #####
    def get_payload(self, row, column, color):
        payload = json.dumps({
            "candidateId": candidateId,
            "row": row,
            "column": column,
            "color": color, 
        })
        return payload
    
class Cometh(AstralObject):
    # available HTTP methods:
    # POST - arguments: row, col, direction
    # DELETE - arguments: row, col

    # class attrs
    endpoint = '/api/comeths'

    # instance attrs
    def __init__(self, index, direction):
        super().__init__()
        self.name='COMETH'
        self.index=index
        self.payload = self.get_payload(index[0], index[1], direction)
        self.direction=direction
        self.url= (self.base + Cometh.endpoint) #overkill as each instance has the same val but kept bc in theory is more scalable

    # #####
    def get_payload(self, row, column, direction):
        payload = json.dumps({
            "candidateId": candidateId,
            "row": row,
            "column": column,
            "direction": direction, 
        })
        return payload

class AstralObjectsAsyncClient():

    def __init__(self, astrallist):
        self.astrallist = astrallist
        self.loop = asyncio.get_event_loop()
        self.future = asyncio.ensure_future(self.run())

    async def fetch(self,url, session, payload, headers):
        async with session.post(url, data=payload, headers=headers) as response:
            # print('fetching', url, payload) #used to see what was going on. can delete. 
            return await response.read()

    async def run(self):
        tasks = []
        # Fetch all responses within one Client session,
        # keep connection alive for all requests.

        # the follwing lines are an alternative way to add rate/resource limits. 
        # async with self.sem:
            # await asyncio.sleep(0.1)


        connector = aiohttp.TCPConnector(limit_per_host=1) #if left unlimited number is ~100 and crossmint api does not like that :(

        async with ClientSession(connector=connector) as session:
            for i in self.astrallist:
                url = i.url
                payload = i.payload
                headers = i.headers

                task = asyncio.ensure_future(self.fetch(url, session, payload, headers))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            # you now have all response bodies in this variable
            # print(responses, tasks) #used to see what was going on. can delete. 


#  main 
if __name__ == "__main__":

    # get current goalmap. currently app is designed that if all phases are done it returns 500. 
    #  so if 500 we return empty map so the universe doesnt explode. 
    goalmap = GoalMap().goalmap


    #goalmap to list of astral objects
    astrallist = AstralObjectsMapper(goalmap).astral_objects

    # start timer
    start_time = time.time()

    # run asyc client
    asyncclient  = AstralObjectsAsyncClient(astrallist)
    asyncclient.loop.run_until_complete(asyncclient.future)

    # timer output
    print("--- %s seconds ---" % (time.time() - start_time))
