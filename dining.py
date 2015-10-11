import asyncio
import random

class Philosopher:
    def __init__(self, name, neighbor):
        self.name = name
        self.chopstick = asyncio.Lock()
        self.neighbor = neighbor

    async def think(self):
        print("%s is thinking...\n" % self.name)
        await asyncio.sleep(random.uniform(0.1, 1))

    async def eat(self):
        print("%s is eating...\n" % self.name)
        await asyncio.sleep(random.uniform(0.1, 1))

    async def get_chopsticks(self):
        print("%s trying to get chopstiks" % self.name)
        try:
            await asyncio.wait_for(self.chopstick.acquire(), 1)
        except asyncio.TimeoutError:
            print("%s failed to get his chopstick" % self.name)
            await self.think()
            await self.get_chopsticks()
            return

        try:
            print("%s trying to get %s's chopstick" % (self.name, self.neighbor.name))
            await asyncio.wait_for(self.neighbor.chopstick.acquire(), 1)
        except asyncio.TimeoutError:
            print("%s failed to get %s's chopstick" % (self.name, self.neighbor.name))
            await self.chopstick.release()
            await self.think()
            await self.get_chopsticks()
            return

        print("%s get all chopsticks" % self.name)
        return

    async def return_chopsticks(self):
        self.chopstick.release()
        self.neighbor.chopstick.release()


    async def dine(self):
        await self.think()
        await self.get_chopsticks()
        await self.eat()
        await self.return_chopsticks()
        return self.name

if __name__ == '__main__':
    names = [
            "Kant", "Heidegger", "Wittgenstein",
            "Locke", "Descartes", "Newton",
            "Hume", "Leibniz"
            ]
    prev_phil = Philosopher(names[0], None)
    philosophers = [prev_phil,]
    for name in names[1:]:
        phil = Philosopher(name, prev_phil)
        prev_phil = phil
        philosophers.append(phil)

    philosophers[0].neighbor = prev_phil

    loop = asyncio.get_event_loop()
    tasks = []
    for p in philosophers:
        tasks.append(asyncio.ensure_future(p.dine()))

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

