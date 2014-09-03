# full_setup.py
# 
# Created:  SUave Team, Aug 2014
# Modified: 

""" setup file for a mission with a 737
"""


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Attributes import Units

import numpy as np
import pylab as plt

import copy, time

from SUAVE.Structure import (
Data, Container, Data_Exception, Data_Warning,
)

def full_setup():

    vehicle = vehicle_setup()
    mission = mission_setup(vehicle)
    
    return vehicle, mission

def vehicle_setup():
    
    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------    
    
    vehicle = SUAVE.Vehicle()
    vehicle.tag = 'Boeing 737-800'    
    
    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    

    # mass properties
    vehicle.Mass_Properties.max_takeoff               = 79015.8   # kg
    vehicle.Mass_Properties.operating_empty           = 62746.4   # kg
    vehicle.Mass_Properties.takeoff                   = 79015.8   # kg
    #vehicle.Mass_Properties.m_flight_min              = 66721.59  # kg
    vehicle.Mass_Properties.max_zero_fuel             = 0.9 * vehicle.Mass_Properties.max_takeoff 
    vehicle.Mass_Properties.center_of_gravity         = [60 * Units.feet, 0, 0]  # Not correct
    vehicle.Mass_Properties.Moments_Of_Inertia.tensor = [[10 ** 5, 0, 0],[0, 10 ** 6, 0,],[0,0, 10 ** 7]] # Not Correct
    vehicle.Mass_Properties.cargo                     = 10000.  * Units.kilogram   
    
    # envelope properties
    vehicle.Envelope.ultimate_load = 3.5
    vehicle.Envelope.limit_load    = 1.5

    # basic parameters
    #vehicle.delta    = 25.0                     # deg
    vehicle.reference_area        = 124.862       
    vehicle.passengers = 170
    #vehicle.A_engine = np.pi*(0.9525)**2
    vehicle.Systems.control  = "fully powered" 
    vehicle.Systems.accessories = "medium range"

    #vehicle.cargo_weight = 10000.  * Units.kilogram    
    
    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------        
    
    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'Main Wing'
    
    wing.Areas.reference = 124.862    #
    wing.aspect_ratio    = 8        #
    wing.Spans.projected = 35.66      #
    wing.sweep           = 25 * Units.deg
    wing.symmetric       = False
    wing.thickness_to_chord = 0.1
    wing.taper           = 0.16
    
    
    # size the wing planform ----------------------------------
    # These can be determined by the wing sizing function
    # Note that the wing sizing function will overwrite span
    wing.Chords.root  = 6.81
    wing.Chords.tip   = 1.09
    wing.Areas.wetted = wing.Areas.reference*2.0 
    # The span that would normally be overwritten here doesn't match
    # ---------------------------------------------------------
    
    wing.Chords.mean_aerodynamic = 12.5
    wing.Areas.exposed = 0.8*wing.Areas.wetted
    wing.Areas.affected = 0.6*wing.Areas.wetted
    wing.span_efficiency = 0.9
    wing.Twists.root = 3.0*Units.degrees
    wing.Twists.tip  = 3.0*Units.degrees
    wing.origin          = [20,0,0]
    wing.aerodynamic_center = [3,0,0] 
    wing.vertical   = False
    wing.eta         = 1.0
    #wing.hl          = 1                    #
    #wing.flaps_chord = 20                   #
    #wing.flaps_angle = 20                   #
    #wing.slats_angle = 10                   #
    
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------        
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------        
    
    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'Horizontal Stabilizer'
    
    wing.Areas.reference = 32.488    #
    wing.aspect_ratio    = 6.16      #
    wing.Spans.projected = 14.146      #
    wing.sweep           = 30 * Units.deg
    wing.symmetric       = True
    wing.thickness_to_chord = 0.08
    wing.taper           = 0.4
    
    # size the wing planform ----------------------------------
    # These can be determined by the wing sizing function
    # Note that the wing sizing function will overwrite span
    wing.Chords.root  = 3.28
    wing.Chords.tip   = 1.31
    wing.Areas.wetted = wing.Areas.reference*2.0 
    # ---------------------------------------------------------
    
    wing.Chords.mean_aerodynamic = 8.0
    wing.Areas.exposed = 0.8*wing.Areas.wetted
    wing.Areas.affected = 0.6*wing.Areas.wetted
    wing.span_efficiency = 0.9
    wing.Twists.root = 3.0*Units.degrees
    wing.Twists.tip  = 3.0*Units.degrees  
    wing.origin          = [50,0,0]
    wing.aerodynamic_center = [2,0,0]
    wing.vertical   = False 
    wing.eta         = 0.9  
    
    # add to vehicle
    vehicle.append_component(wing)
    
    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------
    
    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'Vertical Stabilizer'    
    
    wing.Areas.reference = 32.488    #
    wing.aspect_ratio    = 1.91      #
    wing.Spans.projected = 7.877      #
    wing.sweep           = 25 * Units.deg
    wing.symmetric       = False
    wing.thickness_to_chord = 0.08
    wing.taper           = 0.4
    
    # size the wing planform ----------------------------------
    # These can be determined by the wing sizing function
    # Note that the wing sizing function will overwrite span
    wing.Chords.root  = 6.60
    wing.Chords.tip   = 1.65
    wing.Areas.wetted = wing.Areas.reference*2.0 
    # ---------------------------------------------------------
    
    wing.Chords.mean_aerodynamic = 8.0
    wing.Areas.exposed = 0.8*wing.Areas.wetted
    wing.Areas.affected = 0.6*wing.Areas.wetted
    wing.span_efficiency = 0.9
    wing.Twists.root = 0.0*Units.degrees
    wing.Twists.tip  = 0.0*Units.degrees  
    wing.origin          = [50,0,0]
    wing.aerodynamic_center = [2,0,0]    
    wing.vertical   = True 
    wing.t_tail     = False
    wing.eta         = 1.0
        
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------
    
    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag = 'Fuselage'
    
    fuselage.number_coach_seats = 200
    fuselage.seats_abreast = 6
    fuselage.seat_pitch = 1
    fuselage.Fineness.nose = 1.6
    fuselage.Fineness.tail = 2.
    fuselage.Lengths.fore_space = 6.
    fuselage.Lengths.aft_space  = 5.
    fuselage.width = 4.
    fuselage.Heights.maximum          = 4.    #
    fuselage.Areas.side_projected       = 4.* 59.8 #  Not correct
    fuselage.Heights.at_quarter_length = 4. # Not correct
    fuselage.Heights.at_three_quarters_length = 4. # Not correct
    fuselage.Heights.at_wing_root_quarter_chord = 4. # Not correct
    fuselage.differential_pressure = 10**5   * Units.pascal    # Maximum differential pressure
    
    # size fuselage planform
    # A function exists to do this
    fuselage.Lengths.nose  = 6.4
    fuselage.Lengths.tail  = 8.0
    fuselage.Lengths.cabin = 44.0
    fuselage.Lengths.total = 58.4
    fuselage.Areas.wetted  = 688.64
    fuselage.Areas.front_projected = 12.57
    #fuselage.Areas.front_projected     = 12.57 # ?? CHECK
    fuselage.effective_diameter        = 4.0
    
    # add to vehicle
    vehicle.append_component(fuselage)
    
    # ------------------------------------------------------------------
    #  Turbofan
    # ------------------------------------------------------------------    
    
    turbofan = SUAVE.Components.Propulsors.TurboFanPASS()
    turbofan.tag = 'Turbo Fan'
    
    turbofan.propellant = SUAVE.Attributes.Propellants.Jet_A()
    
    #turbofan.analysis_type                 = '1D'     #
    turbofan.diffuser_pressure_ratio       = 0.98     #
    turbofan.fan_pressure_ratio            = 1.7      #
    turbofan.fan_nozzle_pressure_ratio     = 0.99     #
    turbofan.lpc_pressure_ratio            = 1.14     #
    turbofan.hpc_pressure_ratio            = 13.415   #
    turbofan.burner_pressure_ratio         = 0.95     #
    turbofan.turbine_nozzle_pressure_ratio = 0.99     #
    turbofan.Tt4                           = 1450.0   #
    turbofan.bypass_ratio                  = 5.4      #
    turbofan.Thrust.design                 = 25000.0  #
    turbofan.number_of_engines             = 2.0      #
    
    # size the turbofan
    turbofan.A2          =   1.753
    turbofan.df          =   1.580
    turbofan.nacelle_dia =   1.580
    turbofan.A2_5        =   0.553
    turbofan.dhc         =   0.857
    turbofan.A7          =   0.801
    turbofan.A5          =   0.191
    turbofan.Ao          =   1.506
    turbofan.mdt         =   9.51
    turbofan.mlt         =  22.29
    turbofan.mdf         = 355.4
    turbofan.mdlc        =  55.53
    turbofan.D           =   1.494
    turbofan.mdhc        =  49.73  
    
    # add to vehicle
    vehicle.append_component(turbofan)    
    
    # ------------------------------------------------------------------
    #   Simple Aerodynamics Model
    # ------------------------------------------------------------------ 
    
    aerodynamics = SUAVE.Attributes.Aerodynamics.Fidelity_Zero()
    aerodynamics.initialize(vehicle)
    
    # build stability model
    stability = SUAVE.Attributes.Flight_Dynamics.Fidelity_Zero()
    stability.initialize(vehicle)
    aerodynamics.stability = stability
    vehicle.aerodynamics_model = aerodynamics
    
    # ------------------------------------------------------------------
    #   Simple Propulsion Model
    # ------------------------------------------------------------------     
    
    vehicle.propulsion_model = vehicle.Propulsors

    # ------------------------------------------------------------------
    #   Define Configurations
    # ------------------------------------------------------------------

    # --- Takeoff Configuration ---
    config = vehicle.new_configuration("takeoff")
    # this configuration is derived from the baseline vehicle

    # --- Cruise Configuration ---
    config = vehicle.new_configuration("cruise")
    # this configuration is derived from vehicle.Configs.takeoff

    # --- Takeoff Configuration ---
    takeoff_config = vehicle.Configs.takeoff
    takeoff_config.Wings['Main Wing'].flaps_angle =  20. * Units.deg
    takeoff_config.Wings['Main Wing'].slats_angle  = 25. * Units.deg
    # V2_V2_ratio may be informed by user. If not, use default value (1.2)
    takeoff_config.V2_VS_ratio = 1.21
    # CLmax for a given configuration may be informed by user. If not, is calculated using correlations
    takeoff_config.maximum_lift_coefficient = 2.
    #takeoff_config.max_lift_coefficient_factor = 1.0

    # --- Landing Configuration ---
    landing_config = vehicle.new_configuration("landing")
    landing_config.Wings['Main Wing'].flaps_angle =  30. * Units.deg
    landing_config.Wings['Main Wing'].slats_angle  = 25. * Units.deg
    # Vref_V2_ratio may be informed by user. If not, use default value (1.23)
    landing_config.Vref_VS_ratio = 1.23
    # CLmax for a given configuration may be informed by user
    landing_config.maximum_lift_coefficient = 2.
    #landing_config.max_lift_coefficient_factor = 1.0
    landing_config.Mass_Properties.m_landing = 0.85 * vehicle.Mass_Properties.takeoff
    

    # ------------------------------------------------------------------
    #   Vehicle Definition Complete
    # ------------------------------------------------------------------
    
    return vehicle    


# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
def mission_setup(vehicle):
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = SUAVE.Attributes.Missions.Mission()
    mission.tag = 'The Test Mission'

    # initial mass
    mission.m0 = vehicle.Mass_Properties.takeoff # linked copy updates if parent changes
    
    # atmospheric model
    planet = SUAVE.Attributes.Planets.Earth()
    atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    mission.airport = airport
    
    
    # ------------------------------------------------------------------
    #   First Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------
    
    segment = SUAVE.Attributes.Missions.Segments.Climb.Constant_Speed_Constant_Rate()
    segment.tag = "Climb - 1"
    
    # connect vehicle configuration
    segment.config = vehicle.Configs.takeoff
    
    # define segment attributes
    segment.atmosphere     = atmosphere
    segment.planet         = planet    
    
    segment.altitude_start = 0.0   * Units.km
    segment.altitude_end   = 3.0   * Units.km
    segment.air_speed      = 125.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']
    
    # add to misison
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------
    #   Second Climb Segment: constant Speed, constant segment angle 
    # ------------------------------------------------------------------    
    
    segment = SUAVE.Attributes.Missions.Segments.Climb.Constant_Speed_Constant_Rate()
    #segment = SUAVE.Attributes.Missions.Segments.Climb.Constant_Mach_Constant_Rate()
    segment.tag = "Climb - 2"
    
    # connect vehicle configuration
    segment.config = vehicle.Configs.cruise
    
    # segment attributes
    segment.atmosphere     = atmosphere
    segment.planet         = planet    
    
    #segment.altitude_start = 3.0   * Units.km ## Optional
    segment.altitude_end   = 8.0   * Units.km
    segment.air_speed      = 190.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']
    #segment.mach_number    = 0.5
    #segment.climb_rate     = 6.0   * Units['m/s']
    
    # add to mission
    mission.append_segment(segment)

    
    # ------------------------------------------------------------------
    #   Third Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------    
    
    segment = SUAVE.Attributes.Missions.Segments.Climb.Constant_Speed_Constant_Rate()
    segment.tag = "Climb - 3"
    
    # connect vehicle configuration
    segment.config = vehicle.Configs.cruise
    
    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet        
    
    segment.altitude_end = 10.668 * Units.km
    segment.air_speed    = 226.0  * Units['m/s']
    segment.climb_rate   = 3.0    * Units['m/s']
    
    # add to mission
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------    
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------    
    
    segment = SUAVE.Attributes.Missions.Segments.Cruise.Constant_Speed_Constant_Altitude()
    segment.tag = "Cruise"
    
    # connect vehicle configuration
    segment.config = vehicle.Configs.cruise
    
    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet     = planet        
    
    #segment.altitude   = 10.668  * Units.km     # Optional
    segment.air_speed  = 230.412 * Units['m/s']
    segment.distance   = 3933.65 * Units.km
        
    mission.append_segment(segment)

    # ------------------------------------------------------------------    
    #   First Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------    

    segment = SUAVE.Attributes.Missions.Segments.Descent.Constant_Speed_Constant_Rate()
    segment.tag = "Descent - 1"
    
    # connect vehicle configuration
    segment.config = vehicle.Configs.cruise
    
    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet   
    
    segment.altitude_end = 5.0   * Units.km
    segment.air_speed    = 170.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']
    
    # add to mission
    mission.append_segment(segment)
    

    # ------------------------------------------------------------------    
    #   Second Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------    

    segment = SUAVE.Attributes.Missions.Segments.Descent.Constant_Speed_Constant_Rate()
    segment.tag = "Descent - 2"

    # connect vehicle configuration
    segment.config = vehicle.Configs.cruise

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet    
    
    segment.altitude_end = 0.0   * Units.km
    segment.air_speed    = 145.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']

    # append to mission
    mission.append_segment(segment)

    
    # ------------------------------------------------------------------    
    #   Mission definition complete    
    # ------------------------------------------------------------------
    
    return mission


if __name__ == '__main__': 
    
    full_setup()