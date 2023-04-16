import asyncio
from pywizlight import wizlight, PilotBuilder, scenes
from time import sleep

# List of IP addresses of bulbs (get from WiZ app)
# Manual as UDP discovery doesn't seem to work
ips = ["10.247.63.188"]

class WizLightModule:

    def __init__(self, bulbs_ip=ips):
        bulbs = []
        for ip in bulbs_ip:
            bulbs.append(wizlight(ip))
        self.lights = bulbs

    # Into rhythm mode
    async def turn_on(self):
        async def _turn_on(light):
            await light.turn_on(PilotBuilder())
        try:
            await self.sync_execute(_turn_on)
        except Exception as e:
            print(e)

    async def turn_off(self):
        async def _turn_off(light):
            await light.turn_off()
        try:
            await self.sync_execute(_turn_off)
        except Exception as e:
            print(e)

    async def set_warm_light(self):
        async def _set_warm(light):
            await light.turn_on(PilotBuilder(warm_white=255))
        try:
            await self.sync_execute(_set_warm)
        except Exception as e:
            print(e)

    async def set_cool_light(self):
        async def _set_cool(light):
            await light.turn_on(PilotBuilder(cold_white=255))
        try:
            await self.sync_execute(_set_cool)
        except Exception as e:
            print(e)

    async def set_scene(self, scene_name):
        async def _set_scene(light, scene_id):
            await light.turn_on(PilotBuilder(scene=scene_id))
        try:
            scene_id = scenes.get_id_from_scene_name(scene_name)
            await self.sync_execute(_set_scene, scene_id=scene_id)
        except Exception as e:
            print(e)
    

    # Utility functions

    # Rasa calls each action in a different loop, so the running loops of the bulbs must be updated
    def _update_loops(self):
        for light in self.lights:
            light.loop = asyncio.get_running_loop()
            light.transport = None # The Datagram endpoint will be attached to the wrong loop

    # Gather the async tasks for synchronised execution (for multiple bulbs)
    async def sync_execute(self, f, **kwargs):
        self._update_loops()
        return await asyncio.gather(*[f(light, **kwargs) for light in self.lights])

    async def get_states(self):
        async def _get_state(light):
            state = await light.updateState()
            return state
        return await self.sync_execute(_get_state)

    async def check_connection(self):
        states = await self.get_states()
        connections = len(states)
        if connections == 1:
            print('1 Wizlight connected.')
        elif connections > 1:
            print(f'{connections} Wizlights Connected.')
        else:
            raise Exception('No Wizlights connected. Check your list of Wizlight IP addresses.')


# Testing

async def main():
    mod = WizLightModule()
    await mod.set_scene('Cozy')
    states = await mod.get_states()
    print(states)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())