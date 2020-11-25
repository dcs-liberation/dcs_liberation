--F-22A by Grinnellidesigns - Version 4 - 4-23-19
F_22A =  {
      
		Name 			= 'F-22A',--AG
		DisplayName		= _('F-22A'),--AG
        Picture 		= "F-22A.png",
        Rate 			= "50",
        Shape			= "F-22A",--AG	
        WorldID			=  WSTYPE_PLACEHOLDER, 
        
	shape_table_data 	= 
	{
		{
			file  	 	= 'F-22A';--AG
			life  	 	= 20; -- lifebar
			vis   	 	= 2; -- visibility gain.
			desrt    	= 'F-22A_destr'; -- Name of destroyed object file name
			fire  	 	= { 300, 2}; -- Fire on the ground after destoyed: 300sec 2m
			username	= 'F-22A';--AG
			index       =  WSTYPE_PLACEHOLDER;
			classname   = "lLandPlane";
			positioning = "BYNORMAL";
		},
		{
			name  		= "F-22A_destr";
			file  		= "F-22A_destr";
			fire  		= { 240, 2};
		},
	},
	
	LandRWCategories = 
        {
        [1] = 
        {
			Name = "AircraftCarrier",
        },
        [2] = 
        {
            Name = "AircraftCarrier With Catapult",
        }, 
        [3] = 
        {
            Name = "AircraftCarrier With Tramplin",
        }, 
    },
        TakeOffRWCategories = 
        {
        [1] = 
        {
			Name = "AircraftCarrier",
        },
        [2] = 
        {
            Name = "AircraftCarrier With Catapult",
        }, 
        [3] = 
        {
            Name = "AircraftCarrier With Tramplin",
        }, 
    },
	
	Countries = {"USA","USAF Aggressors"},
	
	
	mapclasskey 		= "P0091000024",
	--attribute  			= {wsType_Air, wsType_Airplane, wsType_Fighter, F_15, "Fighters", "Refuelable",},--AG WSTYPE_PLACEHOLDER
	attribute  			= {wsType_Air, wsType_Airplane, wsType_Fighter, F_22A, "Fighters", "Refuelable",},--AG WSTYPE_PLACEHOLDER
	Categories= {"{78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}", "Interceptor",},
	
		M_empty						=	13380,	-- kg  with pilot and nose load, F15
		M_nominal					=	19000,	-- kg (Empty Plus Full Internal Fuel)
		M_max						=	30845,	-- kg (Maximum Take Off Weight)
		M_fuel_max					=	6103,	-- kg (Internal Fuel Only)
		H_max						=	18300,	-- m  (Maximum Operational Ceiling)
		average_fuel_consumption	=	0.21,
		CAS_min						=	58,		-- Minimum CAS speed (m/s) (for AI)
		V_opt						=	220,	-- Cruise speed (m/s) (for AI)
		V_take_off					=	61,		-- Take off speed in m/s (for AI)
		V_land						=	71,		-- Land speed in m/s (for AI)
		has_afteburner				=	true,
		has_speedbrake				=	true,
		radar_can_see_ground		=	true,

		--nose_gear_pos 				                = {5.981,	-1.906,	0},   --{6.30,	-1.75,	0},
		---nose_gear_pos 				                = {-0.001,	-1.707,	4.032},   --{6.30,	-1.75,	0},
	    --nose_gear_amortizer_direct_stroke   		= -0.118,      -- down from nose_gear_pos !!!
	    --nose_gear_amortizer_reversal_stroke  		=  0.317,      -- up 
	    --nose_gear_amortizer_normal_weight_stroke 	= -0.199,      -- down from nose_gear_pos
	    --nose_gear_wheel_diameter 	                =  0.674,  -- in m .754
	
	    --main_gear_pos 						 	    = {-0.472,	-1.685,	1.598},-- maingear coord {-1.598,	-1.685,	2.380},
		---main_gear_pos 						 	    = {2.380,	-1.685,	-1.598},-- maingear coord
	    --main_gear_amortizer_direct_stroke	 	    =  -0.228,     --  down from main_gear_pos !!! -0.228
	    --main_gear_amortizer_reversal_stroke  	    =  0.221,     --  up 0.221
	    --main_gear_amortizer_normal_weight_stroke    =  -0.228,     --  down from main_gear_pos -0.228
	    --main_gear_wheel_diameter 				    =   0.972, --  in m  
		
		nose_gear_pos 				                = {5.981,	-1.707,	0},   --{6.30,	-1.75,	0},
		--nose_gear_pos 				                = {-0.001,	-1.707,	4.032},   --{6.30,	-1.75,	0},
	    nose_gear_amortizer_direct_stroke   		=  0,      -- down from nose_gear_pos !!!
	    nose_gear_amortizer_reversal_stroke  		= -0,      -- up 
	    nose_gear_amortizer_normal_weight_stroke 	= -0,      -- down from nose_gear_pos
	    nose_gear_wheel_diameter 	                =  0.754,  -- in m
	
	    main_gear_pos 						 	    = {-1.598,	-1.585,	2.380},-- maingear coord
		--main_gear_pos 						 	    = {2.380,	-1.685,	-1.598},-- maingear coord
	    main_gear_amortizer_direct_stroke	 	    =   0,     --  down from main_gear_pos !!!
	    main_gear_amortizer_reversal_stroke  	    =  -0,     --  up 
	    main_gear_amortizer_normal_weight_stroke  =  -0,     --  down from main_gear_pos
	    main_gear_wheel_diameter 				    =   0.972, --  in m
		
		effects_presets =   { 
							{effect = "OVERWING_VAPOR", file = current_mod_path.."/Effects/F-22A_overwingVapor.lua"},
							},

		AOA_take_off				=	0.16,	-- AoA in take off (for AI)
		stores_number				=	11,
		bank_angle_max				=	60,		-- Max bank angle (for AI)
		Ny_min						=	-3,		-- Min G (for AI)
		Ny_max						=	8,		-- Max G (for AI)
		tand_gear_max				=	3.73,	--XX  FA18 3.73, 
		V_max_sea_level				=	403,	-- Max speed at sea level in m/s (for AI)
		V_max_h						=	736.11,	-- Max speed at max altitude in m/s (for AI)
		wing_area					=	56.5,	-- wing area in m2
		thrust_sum_max				=	13347,	-- thrust in kgf (64.3 kN)
		thrust_sum_ab				=	21952,	-- thrust in kgf (95.1 kN)
		Vy_max						=	275,	-- Max climb speed in m/s (for AI)
		flaps_maneuver				=	1,
		Mach_max					=	2.5,	-- Max speed in Mach (for AI)
		range						=	2540,	-- Max range in km (for AI)
		RCS							=	0.0001,		-- Radar Cross Section m2
		Ny_max_e					=	8,		-- Max G (for AI)
		detection_range_max			=	250,
		IR_emission_coeff			=	0.85,	-- Normal engine -- IR_emission_coeff = 1 is Su-27 without afterburner. It is reference.
		IR_emission_coeff_ab		=	2.3,		-- With afterburner
		tanker_type					=	2,--F14=2/S33=4/M29=0/S27=0/F15=1/F16=1/To=0/F18=2/A10A=1/M29K=4/M2000=2/F4=0/F5=0/
		wing_span					=	13.05,--XX   wing spain in m 13.05 19.54 
		wing_type 					= 	1,-- 0=FIXED_WING/ 1=VARIABLE_GEOMETRY/ 2=FOLDED_WING/ 3=ARIABLE_GEOMETRY_FOLDED
		length						=	19.1,--XX
		height						=	4.88,--XX
		crew_size					=	1, --XX
		engines_count				=	2, --XX
		wing_tip_pos 				= 	{-4.366,	0.45,	6.357},-- wingtip coords for visual effects
		
		EPLRS 					    = true,--can you be seen on the A-10C TAD Page?
		TACAN_AA					= true,--I think this will not work for a client slot but AI might add a TACAN for the unit.

		sound_name	=	"aircraft\F-22A\Sounds",
		
		engines_nozzles = 
		{
			[1] = 
			{
				pos = 	{-6.901,	0.000,	-1.45},
				elevation	=	-0.3,          -- AFB cone elevation  
				diameter	=	1.02,          --1.072 AFB cone diameter
				exhaust_length_ab	=	8.629, --8.629 lenght in m
				exhaust_length_ab_K	=	0.76,  --0.76 AB animation
				smokiness_level     = 	0.01,
			}, -- end of engine [1]
			[2] = 
			{
				pos = 	{-6.901,	0.000,	1.45},---6.701,	-0.215,	1.524  Tribwerke
				elevation	=	-0.3,--0
				diameter	=	1.02,--1.072
				exhaust_length_ab	=	8.629,--8.629
				exhaust_length_ab_K	=	0.76,
				smokiness_level     = 	0.01, 
			}, -- end of [2]
		}, -- end of engines_nozzles
		
		crew_members = 
		{
			[1] = 
			{
				ejection_seat_name	=	17,--17=FA-18 58=F-15
				drop_canopy_name	=	"F-22A_Canopy";  --need to update this .EDM file for it to work again.
				pos = 	{6.49,	0.94,	0},
			},
		},
		
		brakeshute_name	=	0,
		is_tanker	=	false,
		air_refuel_receptacle_pos = 	{8.319,	0.803,	1.148},
		
		fires_pos = 
		{
			[1] = 	{ 0.931,	0.811,	 0}, -- Body center ?
			[2] = 	{-0.132,		0.390, 	 2.576}, --Left wing fire? {-2.0,		0.8, 	 3.4},
			[3] = 	{-0.132,		0.390,	-2.576}, --Right wing fire?
			[4] = 	{-0.82,	    0.265,	 2.774},
			[5] = 	{-0.82,	    0.265,	-2.774},
			[6] = 	{-0.82,	    0.255,	 4.274},
			[7] = 	{-0.82,	    0.255,	-4.274},
			[8] = 	{-4.593,	   0.242,	 0.639}, --engine fire L
			[9] = 	{-4.593,	   0.242,	-0.639}, --engine fire R
			[10] = 	{-0.515,	0.807,	 0.7},
			[11] = 	{-0.515,	0.807,	-0.7},
		}, -- end of fires_pos
		
		chaff_flare_dispenser = 
		{
			[1] = 
			{
				dir = 	{0,	0,	0},
				pos = 	{-1.453,	-0.406,	1.467}, --{-1.453,	-0.206,	1.467},
			}, 
			[2] = 
			{
				dir = 	{0,	0,	0},
				pos = 	{-1.453,	-0.406,	-1.467}, --{-3.776,	-2.0,	0.422},
			}, 
		}, 

-- Countermeasures 
		passivCounterm = {
			CMDS_Edit = true,
			SingleChargeTotal = 240,
			-- RR-170
			chaff = {default = 120, increment = 30, chargeSz = 1},
			-- MJU-7
			flare = {default = 120, increment = 15, chargeSz = 2}
        },
	
        CanopyGeometry 	= {
            azimuth 	= {-145.0, 145.0},-- pilot view horizontal (AI)
            elevation 	= {-50.0, 90.0}-- pilot view vertical (AI)
        },

Sensors 		= {
RADAR 			= "AN/APG-63",--F15
IRST 			= "OLS-27",
OPTIC 			= {"TADS DTV", "TADS DVO", "TADS FLIR"},
RWR 			= "Abstract RWR"--F15
},
Countermeasures = {
ECM 			= "AN/ALQ-135"--F15
},
	Failures = {
			{ id = 'asc', 		label = _('ASC'), 		enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'autopilot', label = _('AUTOPILOT'), enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'hydro',  	label = _('HYDRO'), 	enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'l_engine',  label = _('L-ENGINE'), 	enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'r_engine',  label = _('R-ENGINE'), 	enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'radar',  	label = _('RADAR'), 	enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
		  --{ id = 'eos',  		label = _('EOS'), 		enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
		  --{ id = 'helmet',  	label = _('HELMET'), 	enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'mlws',  	label = _('MLWS'), 		enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'rws',  		label = _('RWS'), 		enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'ecm',   	label = _('ECM'), 		enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'hud',  		label = _('HUD'), 		enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },
			{ id = 'mfd',  		label = _('MFD'), 		enable = false, hh = 0, mm = 0, mmint = 1, prob = 100 },		
	},
	HumanRadio = {
		frequency 		= 127.5,  -- Radio Freq
		editable 		= true,
		minFrequency	= 100.000,
		maxFrequency 	= 156.000,
		modulation 		= MODULATION_AM
	},

Guns = {gun_mount("M_61", { count = 620 },{muzzle_pos = {0.50000, 0.500000, -0.000000}})},   --M_61 is F-15C Mounted Gun

--pylons_enumeration = {1, 11, 10, 2, 3, 9, 4, 8, 5, 7, 6},
--pylons_enumeration = {2, 1, 3, 4, 5, 6, 7, 8, 9, 11, 10},  --test for new setup
pylons_enumeration = {1, 11, 10, 2, 3, 9, 4, 5, 7, 8, 6},
	
	Pylons =     {

        pylon(1, 0, 1.342000, 0.183859, -3.17000, --Left Side Bay
            {
				use_full_connector_position = true,
            },
            {
				{ CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" }, --aim 9X
            }
        ),
        pylon(2, 1, -0.210, -0.9, -1.487,--Left Wing Pylon
            {
				use_full_connector_position = true,
				arg 	  		= 309,
				arg_increment = 1,
            },
            {
			    { CLSID = "{E1F29B21-F291-4589-9FD8-3272EEC69506}" ,arg_value = 0,Cx_gain = 1/2.2},--F-15C Fuel Tank 600 Gallons
				{ CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" ,arg_value = 0,Cx_gain = 1/2.2}, --aim 9X
				{ CLSID = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}" ,arg_value = 0,Cx_gain = 1/2.2}, --aim 9M
				{ CLSID = "{40EF17B7-F508-45de-8566-6FFECC0C1AB8}" ,arg_value = 0,Cx_gain = 1/2.2}, --AIM_120C
				--{ CLSID = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}" ,arg_value = 0,Cx_gain = 1/2.2}, -- MK-82 Test Bomb
				{ CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E741}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - red
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E742}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - green
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E743}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - blue
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E744}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - white
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E745}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - yellow
				{ CLSID = "{5335D97A-35A5-4643-9D9B-026C75961E52}" ,arg_value = 0,Cx_gain = 1/2.2}, --CBU-97 TEST

   				  { CLSID = "{F376DBEE-4CAE-41BA-ADD9-B2910AC95DEC}" ,arg_increment = 0.0},--Fuel tank
				{ CLSID = "LAU-115_2*LAU-127_AIM-9M" ,arg_increment = 0.7},	-- 2xAIM-9M
				{ CLSID = "LAU-115_2*LAU-127_AIM-9X" ,arg_increment = 0.7},	-- 2xAIM-9X
 				{ CLSID = "LAU-115_2*LAU-127_AIM-120C",arg_increment = 0.7}, -- AIM-120


            }
        ),
        pylon(3, 1, 1.2, -0.1, -2.95,--Weapons Bay Left 1
            {
				use_full_connector_position = true,
            },
            {
                { CLSID = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}" }, --aim 9M
                { CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" }, --Aim 9X
				{ CLSID = "{40EF17B7-F508-45de-8566-6FFECC0C1AB8}" }, --AIM_120C
				--{ CLSID = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}" }, -- MK-82 Test Bomb
				{ CLSID = "{5335D97A-35A5-4643-9D9B-026C75961E52}" }, --CBU-97 TEST
            }
        ),
        pylon(4, 1, 2.649, -0.48, -0.37,--Weapons Bay Left 2
            {
				use_full_connector_position = true,
				arg 	  		= 311,
				arg_increment = 1,
            },
            {
				{ CLSID = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}" }, --aim 9M
                { CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" }, --Aim 9X
				{ CLSID = "{40EF17B7-F508-45de-8566-6FFECC0C1AB8}" }, --AIM_120C
				--{ CLSID = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}" }, -- MK-82 Test Bomb
				{ CLSID = "{5335D97A-35A5-4643-9D9B-026C75961E52}" }, --CBU-97 TEST
            }
        ),
        pylon(5, 1, -2.083, -0.30, -0.37,--Weapons Bay Left 3
            {
				use_full_connector_position = true,
				arg 	  		= 312,
				arg_increment = 1,
            },
            {
                { CLSID = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}" }, --aim 9M
                { CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" }, --Aim 9X
				{ CLSID = "{40EF17B7-F508-45de-8566-6FFECC0C1AB8}" }, --AIM_120C
				--{ CLSID = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}" }, -- MK-82 Test Bomb
				{ CLSID = "{5335D97A-35A5-4643-9D9B-026C75961E52}" }, --CBU-97 TEST
            }
        ),
        pylon(6, 1, 1.6, -0.31, 0,--SMOKE POD CENTER REAR HIDDEN
            {
				use_full_connector_position = true,
            },
            {
				{ CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E741}" }, --Smokewinder - red
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E742}" }, --Smokewinder - green
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E743}" }, --Smokewinder - blue
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E744}" }, --Smokewinder - white
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E745}" }, --Smokewinder - yellow
            }
        ),
        pylon(7, 1, -2.083, -0.30, 0.37,--Weapons Bay Right 3
            {
				use_full_connector_position = true,
				arg 	  		= 312,
				arg_increment = 1,
            },
            {
                { CLSID = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}" }, --aim 9M
                { CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" }, --Aim 9X
				{ CLSID = "{40EF17B7-F508-45de-8566-6FFECC0C1AB8}" }, --AIM_120C
				--{ CLSID = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}" }, -- MK-82 Test Bomb
				{ CLSID = "{5335D97A-35A5-4643-9D9B-026C75961E52}" }, --CBU-97 TEST
            }
        ),
        pylon(8, 1, 2.649, -0.48, 0.37,--Weapons Bay Right 2
            {
				use_full_connector_position = true,
				arg 	  		= 311,
				arg_increment = 1,
            },
            {
                { CLSID = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}" }, --aim 9M
                { CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" }, --Aim 9X
				{ CLSID = "{40EF17B7-F508-45de-8566-6FFECC0C1AB8}" }, --AIM_120
				--{ CLSID = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}" }, -- MK-82 Test Bomb
				{ CLSID = "{5335D97A-35A5-4643-9D9B-026C75961E52}" }, --CBU-97 TEST
            }
        ),
		pylon(9, 1, 1.2, -0.1, 2.95,--Weapons Bay Right 1
            {
				use_full_connector_position = true,
            },
            {
                { CLSID = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}" }, --aim 9M
                { CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" }, --Aim 9X
				{ CLSID = "{40EF17B7-F508-45de-8566-6FFECC0C1AB8}" }, --AIM_120C
				--{ CLSID = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}" }, -- MK-82 Test Bomb
				{ CLSID = "{5335D97A-35A5-4643-9D9B-026C75961E52}" }, --CBU-97 TEST
            }
        ),
		pylon(10, 1, -0.210, -0.9, 1.487,--Right Wing Pylon
            {
				use_full_connector_position = true,
				arg 	  		= 317,
				arg_increment = 1,
            },
            {
                { CLSID = "{E1F29B21-F291-4589-9FD8-3272EEC69506}" ,arg_value = 0,Cx_gain = 1/2.2},--F-15C Fuel Tank
				{ CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" ,arg_value = 0,Cx_gain = 1/2.2}, --aim 9X
				{ CLSID = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}" ,arg_value = 0,Cx_gain = 1/2.2}, --aim 9M
				{ CLSID = "{40EF17B7-F508-45de-8566-6FFECC0C1AB8}" ,arg_value = 0,Cx_gain = 1/2.2}, --AIM_120C
				--{ CLSID = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}" ,arg_value = 0,Cx_gain = 1/2.2}, -- MK-82 Test Bomb
				{ CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E741}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - red
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E742}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - green
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E743}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - blue
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E744}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - white
			    { CLSID	= "{A4BCC903-06C8-47bb-9937-A30FEDB4E745}" ,arg_value = 0,Cx_gain = 1/2.2}, --Smokewinder - yellow
				{ CLSID = "{5335D97A-35A5-4643-9D9B-026C75961E52}" ,arg_value = 0,Cx_gain = 1/2.2}, --CBU-97 TEST	
                  	{ CLSID = "{F376DBEE-4CAE-41BA-ADD9-B2910AC95DEC}" ,arg_increment = 0.0},--Fuel tank
				{ CLSID = "LAU-115_2*LAU-127_AIM-9M" ,arg_increment = 0.7},	-- 2xAIM-9M
				{ CLSID = "LAU-115_2*LAU-127_AIM-9X" ,arg_increment = 0.7},	-- 2xAIM-9X
 				{ CLSID = "LAU-115_2*LAU-127_AIM-120C",arg_increment = 0.7}, -- AIM-120



			
            }
        ),
		pylon(11, 0, 1.342000, 0.183859, 3.17000,--Right Side Bay
            {
				use_full_connector_position = true,
            },
            {
                { CLSID = "{5CE2FF2A-645A-4197-B48D-8720AC69394F}" }, --Aim 9X
            }
        ),
},
	
	Tasks = {
        aircraft_task(CAP),
     	aircraft_task(Escort),
      	aircraft_task(FighterSweep),
		aircraft_task(Intercept),
		aircraft_task(Reconnaissance),
    },	
	DefaultTask = aircraft_task(CAP),

	SFM_Data = {
	aerodynamics = --F15
		{
			Cy0	=	0,
			Mzalfa	=	6,
			Mzalfadt	=	1,
			kjx = 2.95,
			kjz = 0.00125,
			Czbe = -0.016,
			cx_gear = 0.0268,
			cx_flap = 0.06,
			cy_flap = 0.4,
			cx_brk = 0.06,
			table_data = 
			{
				{0.0,	0.0215,		0.055,		0.08,		0.22,		0.65,	35.0,	1.2 	},
				{0.2,	0.0215,		0.055,		0.08,		0.22,		1.80,	35.0,	1.2     },
				{0.4,	0.0215,		0.055,		0.08,	   	0.22,		3.00,	35.0,	1.2     },
				{0.6,	0.0215,		0.055,		0.05,		0.28,		4.20,	35.0,	1.2     },
				{0.7,	0.0215,		0.055,		0.05,		0.28,		4.20,	33.0,	1.15    },
				{0.8,	0.0215,		0.055,		0.05,		0.28,		4.20,	31.7,	1.1     },
				{0.9,	0.0230,		0.058,		0.09,		0.20,		4.20,	30.1,	1.07    },
				{1.0,	0.0320,		0.062,		0.17,		0.15,		4.20,	28.9,	1.04    },
				{1.1,	0.0430,		0.062,	   	0.235,	0.09,		3.78,	27.4,	1.02    },
				{1.2,	0.0460,		0.062,	   	0.285,	0.08,		2.94,	27.0,	1.00 	},		
				{1.3,	0.0470,		0.06,	   		0.29,		0.10,		2.10,	26.0,	0.92 	},				
				{1.4,	0.0470,		0.056,	   	0.3,		0.136,	1.80,	25.0,	0.80 	},					
				{1.6,	0.0470,		0.052,	   	0.34,		0.21,		1.08,	23.0,	0.7 	},					
				{1.8,	0.0460,		0.042,	   	0.34,		2.43,		0.96,	22.0,	0.55 	},		
				{2.2,	0.0420,		0.037,	   	0.49,		3.5,		0.84, 20.0,	0.37 	},					
				{2.5,	0.0420,		0.033,		0.6,		4.7,		0.84, 9.0,	0.3 	},		
				{3.9,	0.0400,		0.023,		0.9,		6.0,		0.84, 7.0,	0.2		},
			}, -- end of table_data
		}, -- end of aerodynamics
		engine = 
		{
			Nmg	=	60.00001,
			MinRUD	=	0,
			MaxRUD	=	1,
			MaksRUD	=	0.85,
			ForsRUD	=	0.91,
			type	=	"TurboJet",
			hMaxEng	=	19.5,
			dcx_eng	=	0.0114,
			cemax	=	1.24,
			cefor	=	2.56,
			dpdh_m	=	6500,
			dpdh_f	=	16000.0,
			table_data = {
			--   M		Pmax		 Pfor
				{0.0,	153000,		254000},
				{0.2,	125000,		242000},
				{0.4,	122000,		248000},
				{0.6,	137000,		250000},
				{0.7,	139000,		254000},
				{0.8,	141000,		267000},
				{0.9,	152000,		291000},
				{1.0,	156000,		310000},
				{1.1,	146000,		322500},
				{1.2,	125000,		329600},
				{1.3,	111500,		342000},
				{1.4,	 94000,		360000},
				{1.6,	 45000,		381000},
				{1.8,	 25000,		404000},
				{2.2,	 22000,		444000},
				{2.5,	 25000,		468000},
				{3.9,	109000,		372000},
			}, -- end of table_data
		}, -- end of engine
	},


	--damage , index meaning see in  Scripts\Aircrafts\_Common\Damage.lua
	Damage = {
	[0]  = {critical_damage = 5,  args = {146}},
	[1]  = {critical_damage = 3,  args = {296}},
	[2]  = {critical_damage = 3,  args = {297}},
	[3]  = {critical_damage = 8, args = {65}},
	[4]  = {critical_damage = 2,  args = {298}},
	[5]  = {critical_damage = 2,  args = {301}},
	[7]  = {critical_damage = 2,  args = {249}},
	[8]  = {critical_damage = 3,  args = {265}},
	[9]  = {critical_damage = 3,  args = {154}},
	[10] = {critical_damage = 3,  args = {153}},
	[11] = {critical_damage = 1,  args = {167}},
	[12] = {critical_damage = 1,  args = {161}},
	[13] = {critical_damage = 2,  args = {169}},
	[14] = {critical_damage = 2,  args = {163}},
	[15] = {critical_damage = 2,  args = {267}},
	[16] = {critical_damage = 2,  args = {266}},
	[17] = {critical_damage = 2,  args = {168}},
	[18] = {critical_damage = 2,  args = {162}},
	[20] = {critical_damage = 2,  args = {183}},
	[23] = {critical_damage = 5, args = {223}},
	[24] = {critical_damage = 5, args = {213}},
	[25] = {critical_damage = 2,  args = {226}},
	[26] = {critical_damage = 2,  args = {216}},
	[29] = {critical_damage = 5, args = {224}, deps_cells = {23, 25}},
	[30] = {critical_damage = 5, args = {214}, deps_cells = {24, 26}},
	[35] = {critical_damage = 6, args = {225}, deps_cells = {23, 29, 25, 37}},
	[36] = {critical_damage = 6, args = {215}, deps_cells = {24, 30, 26, 38}}, 
	[37] = {critical_damage = 2,  args = {228}},
	[38] = {critical_damage = 2,  args = {218}},
	[39] = {critical_damage = 2,  args = {244}, deps_cells = {53}}, 
	[40] = {critical_damage = 2,  args = {241}, deps_cells = {54}}, 
	[43] = {critical_damage = 2,  args = {243}, deps_cells = {39, 53}},
	[44] = {critical_damage = 2,  args = {242}, deps_cells = {40, 54}}, 
	[51] = {critical_damage = 2,  args = {240}}, 
	[52] = {critical_damage = 2,  args = {238}},
	[53] = {critical_damage = 2,  args = {248}},
	[54] = {critical_damage = 2,  args = {247}},
	[56] = {critical_damage = 2,  args = {158}},
	[57] = {critical_damage = 2,  args = {157}},
	[59] = {critical_damage = 3,  args = {148}},
	[61] = {critical_damage = 2,  args = {147}},
	[82] = {critical_damage = 2,  args = {152}},
	},
	
	DamageParts = 
	{  
		[1] = "F-22A-oblomok-wing-r", -- wing R
		[2] = "F-22A-oblomok-wing-l", -- wing L
		[3] = "F-22A-oblomok-noise", -- nose
		[4] = "F-22A-oblomok-tail-r", -- tail R
		[5] = "F-22A-oblomok-tail-l", -- tail L
	},

		lights_data = { typename = "collection", lights = {
	
    [1] = { typename = "collection", -- WOLALIGHT_STROBES
					lights = {	
						--{typename  = "natostrobelight",	argument_1  = 199, period = 1.2, color = {0.8,0,0}, connector = "RESERV_BANO_1"},--R
						--{typename  = "natostrobelight",	argument_1  = 199, period = 1.2, color = {0.8,0,0}, connector = "RESERV1_BANO_1"},--L
						--{typename  = "natostrobelight",	argument_1  = 199, period = 1.2, color = {0.8,0,0}, connector = "RESERV2_BANO_1"},--H
						--{typename  = "natostrobelight",	argument_1  = 195, period = 1.2, color = {0.8,0,0}, connector = "WHITE_BEACON L"},--195
						--{typename  = "natostrobelight",	argument_1  = 196, period = 1.2, color = {0.8,0,0}, connector = "WHITE_BEACON R"},--196
						--{typename  = "natostrobelight",	argument_1  = 192, period = 1.2, color = {0.8,0,0}, connector = "BANO_0_BACK"},
						--{typename  = "natostrobelight",	argument_1  = 195, period = 1.2, color = {0.8,0,0}, connector = "RED_BEACON L"},
						--{typename  = "natostrobelight",	argument_1  = 196, period = 1.2, color = {0.8,0,0}, connector = "RED_BEACON R"},
						--{typename = "argnatostrobelight", argument = 195, period = 1.2, phase_shift = 0},-- beacon lights
						{typename = "argnatostrobelight", argument = 199, period = 1.2, phase_shift = 0},-- beacon lights
							}
			},
	[2] = { typename = "collection",
					lights = {-- 1=Landing light -- 2=Landing/Taxi light
						{typename = "spotlight", connector = "MAIN_SPOT_PTR", argument = 209, dir_correction = {elevation = math.rad(-1)}},--"MAIN_SPOT_PTR_02","RESERV_SPOT_PTR"
						--{typename = "spotlight", connector = "MAIN_SPOT_PTR", argument = 208, dir_correction = {elevation = math.rad(3)}},--"MAIN_SPOT_PTR_01","RESERV_SPOT_PTR","MAIN_SPOT_PTL",
							}
			},
    [3]	= {	typename = "collection", -- nav_lights_default
					lights = {
						{typename  = "omnilight",connector =  "BANO_1"  ,argument  =  190,color = {0.99, 0.11, 0.3}},-- Left Position(red)
						{typename  = "omnilight",connector =  "BANO_2"  ,argument  =  191,color = {0, 0.894, 0.6}},-- Right Position(green)
						--{typename  = "omnilight",connector =  "BANO_0"  ,argument  =  192,color = {1, 1, 1}},-- Tail Position white)
							}
			},
	[4] = { typename = "collection", -- formation_lights_default
					lights = {
						--{typename  = "argumentlight" ,argument  = 200,},--formation_lights_tail_1 = 200;
						--{typename  = "argumentlight" ,argument  = 201,},--formation_lights_tail_2 = 201;
						--{typename  = "argumentlight" ,argument  = 202,},--formation_lights_left   = 202;
						--{typename  = "argumentlight" ,argument  = 203,},--formation_lights_right  = 203;
						{typename  = "argumentlight" ,argument  =  88,},--old aircraft arg 
							}
			},
--[[			
	[5] = { typename = "collection", -- strobe_lights_default
					lights = {
						{typename  = "strobelight",connector =  "RED_BEACON"  ,argument = 193, color = {0.8,0,0}},-- Arg 193, 83,
						{typename  = "strobelight",connector =  "RED_BEACON_2",argument = 194, color = {0.8,0,0}},-- (-1"RESERV_RED_BEACON")
						{typename  = "strobelight",connector =  "RED_BEACON"  ,argument =  83, color = {0.8,0,0}},-- Arg 193, 83,
							}
			},
--]]			
	}},
}

add_aircraft(F_22A)