import datetime

from dcs import Mission
from dcs.terrain import Caucasus
from dcs.vehicles import AirDefence

from game import Game
from gen.sam.sam_avenger import AvengerGenerator
from gen.sam.sam_chaparral import ChaparralGenerator
from gen.sam.sam_gepard import GepardGenerator
from gen.sam.sam_hawk import HawkGenerator
from gen.sam.sam_linebacker import LinebackerGenerator
from gen.sam.sam_patriot import PatriotGenerator
from gen.sam.sam_rapier import RapierGenerator
from gen.sam.sam_roland import RolandGenerator
from gen.sam.sam_sa10 import SA10Generator
from gen.sam.sam_sa11 import SA11Generator
from gen.sam.sam_sa13 import SA13Generator
from gen.sam.sam_sa15 import SA15Generator
from gen.sam.sam_sa19 import SA19Generator
from gen.sam.sam_sa2 import SA2Generator
from gen.sam.sam_sa3 import SA3Generator
from gen.sam.sam_sa6 import SA6Generator
from gen.sam.sam_sa8 import SA8Generator
from gen.sam.sam_sa9 import SA9Generator
from gen.sam.sam_zsu23 import ZSU23Generator
from gen.sam.sam_zu23 import ZU23Generator
from gen.sam.sam_zu23_ural import ZU23UralGenerator
from theater import TheaterGroundObject
from theater.caucasus import WesternGeorgia

ter = Caucasus()
m = Mission()



game = Game("USA 1990", "Iran 2015", WesternGeorgia(), datetime.datetime.now())

generated_groups = []

for i,c in enumerate([SA3Generator, SA2Generator, SA6Generator, RapierGenerator,
                      HawkGenerator, SA10Generator, SA19Generator, ZU23Generator,
                      SA8Generator, SA11Generator, SA9Generator, SA13Generator,
                      ZSU23Generator, SA15Generator, GepardGenerator, RolandGenerator,
                      PatriotGenerator, ZU23UralGenerator, ChaparralGenerator,
                      AvengerGenerator, LinebackerGenerator]):
    t = TheaterGroundObject()
    t.position = ter.kutaisi().position
    t.position.x += i*250
    t.dcs_identifier = "AA"
    gen = c(game, t)
    gen.generate()
    vehicle_group = gen.get_generated_group()
    generated_groups.append(vehicle_group)

for g in generated_groups:
    g.name = m.string(g.name)
    for unit in g.units:
        unit.name = m.string(unit.name)
    m.country("USA").add_vehicle_group(g)

m.save("./test.miz")

