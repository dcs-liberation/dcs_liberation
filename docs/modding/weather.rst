#######
Weather
#######

Weather conditions in DCS Liberation are randomly generated at the start of each
turn. Some of the inputs to that generator (more to come) can be controlled via
the config files in ``resources/weather``.

**********
Archetypes
**********

A weather archetype defines the the conditions for a style of weather, such as
"clear", or "raining". There are currently four archetypes:

1. clear
2. cloudy
3. raining
4. thunderstorm

The odds of each archetype appearing in each season are defined in the theater
yaml files (``resources/theaters/*/info.yaml``).

.. literalinclude:: ../../resources/weather/archetypes/clear.yaml
  :language: yaml
  :linenos:
  :caption: resources/weather/archetypes/clear.yaml

Wind speeds
===========

DCS missions define wind with a speed and heading at each of three altitudes:

1. MSL
2. 2000 meters
3. 8000 meters

Blending between each altitude band is done in a manner defined by DCS.

Liberation randomly generates a direction for the wind at MSL, and each other
altitude band will have wind within +/- 90 degrees of that heading.

Wind speeds can be modded by altering the ``speed`` dict in the archetype yaml.
The only random distribution currently supported is the Weibull distribution, so
all archetypes currently use:

.. code:: yaml

   speed:
     weibull:
       ...

The Weibull distribution has two parameters: a shape and a scale.

The scale is simplest to understand. 63.2% of all outcomes of the distribution
are below the scale parameter.

The shape controls where the peak of the distribution is. See the examples in
the links below for illustrations and guidelines, but generally speaking low
values (between 1 and 2.6) will cause low speeds to be more common, medium
values (around 3) will be fairly evenly distributed around the median, and high
values (greater than 3.7) will cause high speeds to be more common. As wind
speeds tend to be higher at higher altitudes and fairly slow close to the
ground, you typically want a low value for MSL, a medium value for 2000m, and a
high value for 8000m.

For examples, see https://statisticsbyjim.com/probability/weibull-distribution/.
To experiment with different inputs, use Wolfram Alpha, e.g.
https://www.wolframalpha.com/input?i=weibull+distribution+1.5+5.

When generating wind speeds, each subsequent altitude band will have the lower
band's speed added to its scale parameter. That is, for the example above, the
actual scale parameter of ``at_2000m`` will be ``20 + wind speed at MSL``, and
the scale parameter of ``at_8000m`` will be ``20 + wind speed at 2000m``. This
is to ensure that a generally windy day (high wind speed at MSL) will create
similarly high winds at higher altitudes and vice versa.
