# Advanced IADS

TODO General description of how this is integrated

Linking Skynet

The current skynet implementation was completly rewritten and factored out to a class which handles the iads_network within the conflict theater. So units will not be handled according to theire name (e.g. RED|SAM...) anymore. They will be included into the mission via the dcsliberation lua table which the skynet script can iterate through.

It current implementation supports:
- Sam, SamAsEWR
- EWR (including Naval)
- PointDefence of Sams (e.g. SA-15 / Tor for high value sites like S-300 or similar)
- Connection Nodes, Power Sources
- Command Centers

## Basic Mode

The regular IADS Mode does not support ConnectionNodes, PowerSources and Command Centers. All Elements will communicate with each other independent from theire distance.
This is the default skynet mode.

## Advanced Network

TODO The advanced mode brings more realism to the game by adding Connections and Power Sources to all the IADS Elements.
This also brings CommandCenters as the Brain.

The advanced network can be used with 2 different implementations:
1. campaign designers can define the iads completly in the campaign yaml (see "By Config")
2. campaign designers can just place the ground units without a definition in the campaign yaml. Then it will be automatically calculated (see "By Range")

How to define the objects
- 3 New Placeholder Objects
- Advanced TriggerZones 

The IADS supports the following placeholder units in the campaign miz:

| IADS Element    | DCS Unit                      |
|-----------------|-------------------------------|
| Command Center  | Fortification._Command_Center |
| Connection Node | Fortification.Comms_tower_M   |
| Power Source    | Fortification.GeneratorF      |

### By Range

TODO Explain the creation by range
Campaign designers only have to set  `advanced_iads: true` in yaml.  
The iads_network class will calculate connections based on distance circles around connection nodes and power sources. 
The distances are hard coded:
- 15nm for Connection Nodes
- 35nm for Power Sources

### By Config

TODO Explain the config file

Do not add Naval Groups or AWACS flights. they will be added automatically

SAM, EWR and CommandCenters to be defined.
Attach all PowerSources and ConnectionNodes to them

```
version: "9.2" # The Version number increased!
advanced_iads: true # Campaign supports the Advanced IADS, Default is false
iads:
  Sam:
    - name: SAM 1 # This is the GroupName / TriggerName used in the Campaign miz
      connected:
        - PS XY # list all group names of the PowerSource or Connection Node
        - CN XY
    # ... more
  Ewr:
    - name: EWR 1
      connected:
        - PS XY
        - CN XY
    # ... more
  CommandCenter:
    - name: CC BLUE
      connected:
        - PS XY
        - CN XY
    - name: CC RED
      connected:
        - PS XY
        - CN XY
```