# LUA Plugin system

This plugin system was made for injecting LUA scripts in dcs-liberation missions.

The resources for the plugins are stored in the `resources/plugins` folder ; each plugin has its own folder.

## Standard plugins

### The *base* plugin

The *base* plugin contains the scripts that are going to be injected in every dcs-liberation missions.
It is mandatory.

### The *JTACAutolase* plugin

This plugin replaces the vanilla JTAC functionality in dcs-liberation.

### The *VEAF framework* plugin

When enabled, this plugin will inject and configure the VEAF Framework scripts in the mission.

These scripts add a lot of runtime functionalities :

- spawning of units and groups (and portable TACANs)
- air-to-ground missions 
- air-to-air missions
- transport missions
- carrier operations (not Moose)
- tanker move
- weather and ATC
- shelling a zone, lighting it up
- managing assets (tankers, awacs, aircraft carriers) : getting info, state, respawning them if needed
- managing named points (position, info, ATC)
- managing a dynamic radio menu
- managing remote calls to the mission through NIOD (RPC) and SLMOD (LUA sockets)
- managing security (not allowing everyone to do every action)
- define groups templates

For more information, please visit the [VEAF Framework documentation site](https://veaf.github.io/VEAF-Mission-Creation-Tools/) (work in progress)

## Custom plugins

Custom scripts can also be injected by dropping them in the `resources/plugins/custom` folder, and writing a `__plugins.lst` file listing them in order.
See the `__plugins.lst.sample` file for an example.

## New settings pages

![New settings pages](0.png "New settings pages")

Custom plugins can be enabled or disabled in the new *LUA Plugins* settings page.

![LUA Plugins settings page](1.png "LUA Plugins settings page")

For plugins which expose specific options (such as "use smoke" for the *JTACAutoLase* plugin), the *LUA Plugins Options* settings page lists these options.

![LUA Plugins Options settings page](2.png "LUA Plugins settings page")


