import asyncio
from pywizlight import wizlight, PilotBuilder, scenes
from time import sleep

# List of IP addresses of bulbs (get from WiZ app)
# Manual as UDP discovery doesn't seem to work
ips = ["10.254.229.143"]

class WizLightModule:

    def __init__(self, bulbs_ip=ips):
        bulbs = []
        for ip in bulbs_ip:
            bulbs.append(wizlight(ip))
        self.lights = bulbs

    async def sync_execute(self, f, **kwargs):
        return await asyncio.gather(*[f(light, **kwargs) for light in self.lights])

    async def set_warm_light(self):
        async def _set_warm(light):
            await light.turn_on(PilotBuilder(warm_white=255))
        await self.sync_execute(_set_warm)

    async def set_cool_light(self):
        async def _set_cool(light):
            await light.turn_on(PilotBuilder(cold_white=255))
        await self.sync_execute(_set_cool)

    # Into rhythm mode
    async def turn_on(self):
        async def _turn_on(light):
            await light.turn_on(PilotBuilder())
        await self.sync_execute(_turn_on)

    async def turn_off(self):
        async def _turn_off(light):
            await light.turn_off()
        await self.sync_execute(_turn_off)

    async def set_scene(self, scene_name):
        async def _set_scene(light, scene_id):
            await light.turn_on(PilotBuilder(scene=scene_id))
        try:
            scene_id = scenes.get_id_from_scene_name(scene_name)
            await self.sync_execute(_set_scene, scene_id=scene_id)
        except Exception as e:
            print(e)

    async def test(self):
        async def _test(light):
            await light.turn_off()
            sleep(1)
            await light.turn_on(PilotBuilder(rgb=(200, 255, 200)))
            sleep(2)
            await light.turn_on(PilotBuilder(rgb=(200, 200, 255)))
            sleep(2)
            await light.turn_on(PilotBuilder(rgb=(255, 200, 200)))
            sleep(2)
            await light.turn_on(PilotBuilder(warm_white=255))
            sleep(2)
            await light.turn_on(PilotBuilder(cold_white=255))
        await self.sync_execute(_test)

    async def get_states(self):
        async def _get_state(light):
            state = await light.updateState()
            return state.get_rgb()
        return await self.sync_execute(_get_state)

async def main():
    mod = WizLightModule()
    await mod.test()
    states = await mod.get_states()
    print(states)

# Testing

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())