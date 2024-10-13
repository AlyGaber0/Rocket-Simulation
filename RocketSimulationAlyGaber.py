# Rocket Simulation Project
import math

FEET_TO_METER = 3.28
DENSITY_OF_ROCKET = 1.225
ROCKET_SMALL_MASS = 100000
ROCKET_MEDIUM_MASS = 400000
SMALL_ROCKET_FUEL_ECON = 1360
MED_ROCKET_FUEL_ECON = 2000
LARGE_ROCKET_FUEL_ECON = 2721
METAL_COST = 5
FUEL_COST = 6.1
TAX = 1.15
WEIGHT_THRESHOLD_MAXIMUM = 0.05
VOLUME_THRESHOLD_MAXIMUM = 0.4
MAX_BOX_WEIGHT = 500
MIN_BOX_WEIGHT = 20
MIN_BOX_VOLUME = 0.125
GRAVITY_CONSTANT = 9.81


def feet_to_meter(feet):
    """
    Converts a value in feet to meters
    
    Args:
        feet (float): The value in feet to be converted.
    
    Returns:
        float: The equivalent value in meters.
    
    Examples:
    >>> feet_to_meter(10)
    32.8
    >>> feet_to_meter(5.5)
    18.04
    >>> feet_to_meter(0)
    0.0  
    """
    meter_answer = round(feet*FEET_TO_METER, 2)
    return meter_answer


def rocket_volume(radius, height_cone, height_cyl):
    """
    Calculates the total volume of a rocket,
    considering its conical and cylindrical parts.
    
    Args:
        radius (float): The radius of the rocket.
        height_cone (float): The height of the conical section.
        height_cyl (float): The height of the cylindrical section.
    
    Returns:
        float: The total volume of the rocket.
    
    Examples:
    >>> rocket_volume(5, 10, 15)
    1439.9
    >>> rocket_volume(3, 7, 8)
    292.17
    >>> rocket_volume(13.4, 17.6, 3.9)
    5509.42  
    """
    volume_cone = (math.pi*(radius**2))*(height_cone/3)
    volume_cyl = math.pi*(radius**2)*height_cyl
    return round(volume_cone + volume_cyl, 2)


def rocket_area(radius, height_cone, height_cyl):
    """
    Calculates the surface area of the rocket,
    including the conical and cylindrical parts and excluding the
    circlular faces of the main cone.
    
    Args:
        radius (float): The radius of the rocket.
        height_cone (float): The height of the conical section.
        height_cyl (float): The height of the cylindrical section.
    
    Returns:
        float: The total surface area of the rocket.
    
    Examples:
    >>> rocket_area(5, 10, 15)
    725.4
    >>> rocket_area(3, 7, 8)
    250.85
    >>> rocket_area(13.4, 17.6, 3.9)
    1823.68
    """
    area_cone = (math.pi*radius*(radius + math.sqrt(height_cone**2 +radius**2)))
    area_cyl = (2*math.pi*radius*(height_cyl + radius))
    area_circle = area_cone + area_cyl - 2*(math.pi*radius**2)
    return round(area_circle, 2)


def rocket_mass(radius, height_cone, height_cyl):
    """
    Calculates the mass of the rocket given its volume and density.
    
    Args:
        radius (float): The radius of the rocket.
        height_cone (float): The height of the conical section.
        height_cyl (float): The height of the cylindrical section.
    
    Returns:
        float: The total mass of the rocket.
    
    Examples:
    >>> rocket_mass(5, 10, 15)
    1763.88
    >>> rocket_mass(3, 7, 8)
    357.91
    >>> rocket_mass(13.4, 17.6, 3.9)
    6749.04
    """
    rocket_density = rocket_volume(radius, height_cone, height_cyl) *\
                     DENSITY_OF_ROCKET
    return round(rocket_density, 2)
    

def rocket_fuel(radius, height_cone, height_cyl,\
                velocity_e, velocity_i, flight_time):
    """
    Calculates the total fuel needed for the rocket trip
    based on its mass, exhaust and initial velocity, and flight time.
    
    Args:
        radius (float): The radius of the rocket.
        height_cone (float): The height of the conical section.
        height_cyl (float): The height of the cylindrical section.
        velocity_e (float): The exhaust velocity of the rocket.
        velocity_i (float): The initial velocity of the rocket.
        flight_time (float): The duration of the flight in seconds.
    
    Returns:
        float: The total fuel needed for the trip.
    
    Examples:
    >>> rocket_fuel(5, 10, 15, 2500, 3000, 120)
    167292.41
    >>> rocket_fuel(3, 7, 8, 1500, 1800, 100)
    136830.39
    >>> rocket_fuel(11.2, 51.8, 105.7, 123.45, 99.65, 81.94)
    185145.0
    """
    total_fuel = rocket_mass(radius, height_cone, height_cyl)*\
                 (math.e**(velocity_i/velocity_e)-1)
    if rocket_mass(radius, height_cone, height_cyl) < ROCKET_SMALL_MASS:
        total_fuel = total_fuel + (SMALL_ROCKET_FUEL_ECON * flight_time)
    elif rocket_mass(radius, height_cone, height_cyl) < ROCKET_MEDIUM_MASS:
        total_fuel = total_fuel + (MED_ROCKET_FUEL_ECON * flight_time)
    else:
        total_fuel = total_fuel + (LARGE_ROCKET_FUEL_ECON * flight_time)
        
    return round(total_fuel, 2)


def calculate_cost(radius, height_cone, height_cyl, velocity_e,\
                   velocity_i, flight_time, tax):
    """
    Calculates the total cost of a rocket trip based on the
    fuel needed, material needed and tax.

    Args:
        radius (float): The radius of the rocket.
        height_cone (float): The height of the conical section.
        height_cyl (float): The height of the cylindrical section.
        velocity_e (float): The exhaust velocity of the rocket.
        velocity_i (float): The initial velocity of the rocket.
        flight_time (float): The duration of the flight in seconds.
        tax (bool): Whether to apply tax to the cost (True or False).

    Returns:
        float: The total cost of the rocket trip.

    Examples:
    >>> calculate_cost(5, 10, 15, 2500, 3000, 120, True)
    1177727.31
    >>> calculate_cost(3, 7, 8, 1500, 1800, 100, False)
    835919.63
    >>> calculate_cost(11.2, 51.8, 105.7, 123.45, 99.65, 81.94, 1)
    1354550.56
    """
    metal_cost = rocket_area(radius, height_cone, height_cyl) * METAL_COST
    fuel_cost = rocket_fuel(radius, height_cone, height_cyl,\
                            velocity_e, velocity_i, flight_time) * FUEL_COST
    if tax == True:
        cost = (metal_cost + fuel_cost) * TAX
    else:
        cost = (metal_cost + fuel_cost)
    
    return round(cost, 2)


def compute_storage_space(radius, height_cyl):
    """
    Calculates the dimensions of the rocket's storage space.

    Args:
        radius (float): The radius of the rocket.
        height_cyl (float): The height of the cylindrical section.

    Returns:
        tuple: The width, length, and height of the storage space in meters.

    Examples:
    >>> compute_storage_space(5, 15)
    (7.07, 7.07, 7.5)
    >>> compute_storage_space(3, 10)
    (4.24, 4.24, 5.0)
    >>> compute_storage_space(25.6, 94.3)
    (36.2, 36.2, 47.15)
    """
    storage_length = math.sqrt(2)*radius
    storage_width = storage_length 
    storage_height = height_cyl/2
    
    return round(storage_width, 2), round(storage_length, 2),\
           round(storage_height, 2)


def load_rocket(rocket_initial_weight, radius, height_cyl):
    """
    Simulates loading items into the rocket,
    ensuring weight and volume constraints are respected.
    
    Args:
        rocket_initial_weight (float):
            The initial weight of the rocket in kilograms.
        radius (float): The radius of the rocket.
        height_cyl (float): The height of the cylindrical section of the rocket.
    
    Returns:
        float: The total weight of the rocket after loading.
    
    Examples:
    >>>
    
    """
    storage_width, storage_length, storage_height =\
                   compute_storage_space(radius, height_cyl)
    storage_volume = storage_width * storage_length * storage_height
    storage_volume = round(storage_volume, 2)
    total_weight = rocket_initial_weight
    total_volume = storage_volume
    weight_of_all_items = 0
    volume_of_all_items = 0
    
    while total_weight < (rocket_initial_weight +\
                          (rocket_initial_weight*WEIGHT_THRESHOLD_MAXIMUM)) and\
          total_volume < (storage_volume +\
                          (storage_volume * VOLUME_THRESHOLD_MAXIMUM)):
        if ((rocket_initial_weight * WEIGHT_THRESHOLD_MAXIMUM) -\
                   weight_of_all_items) < MIN_BOX_WEIGHT:
                    print("No more items can be added")
                    return round(total_weight, 2)
      
        elif (storage_volume * VOLUME_THRESHOLD_MAXIMUM) -\
                     volume_of_all_items < MIN_BOX_VOLUME:
            print("No more items can be added")
            return round(total_weight, 2)
        
        else:
            item_weight = (input('Please enter the weight of the next item'+\
                ' (type "Done" when you are done filling the rocket): '))
            
            if item_weight == "Done":
                return round(total_weight, 2)
            
            else:
                item_weight = float(item_weight)
                item_width = float(input('Enter item width: '))
                item_length = float(input('Enter item length: '))
                item_height = float(input('Enter item height: '))
                item_volume = (item_width*item_length*item_height)
                weight_of_all_items = weight_of_all_items + item_weight
                volume_of_all_items = volume_of_all_items + item_volume

                if item_weight < MIN_BOX_WEIGHT or item_weight > MAX_BOX_WEIGHT or\
                   weight_of_all_items >\
                   (rocket_initial_weight * WEIGHT_THRESHOLD_MAXIMUM):
                    weight_of_all_items = weight_of_all_items - item_weight
                    print("Item could not be added... please try again...")
                elif item_volume < MIN_BOX_VOLUME or\
                       volume_of_all_items >\
                       (storage_volume * VOLUME_THRESHOLD_MAXIMUM):
                    volume_of_all_items = volume_of_all_items - item_volume
                    print("Item could not be added... please try again...")
                    
                else:
                    total_weight = total_weight + weight_of_all_items
                    total_volume = total_volume + volume_of_all_items

        
        
def projectile_sim(simulation_time, interval, velocity_i, angle):
    """
    Simulates the trajectory of a projectile based on
    initial velocity and angle over time.
    
    Args:
        simulation_time (float): The total duration of the simulation in seconds
        interval (float): The time step interval for the simulation.
        velocity_i (float): The initial velocity of the projectile.
        angle (float): The launch angle in radians.
    
    Returns:
        None: Prints the height at each time step
        or stops if the height is below zero.
    
    Examples:
    >>> projectile_sim(10, 1, 30, 0.785)
    0.0
    16.3
    22.79
    19.47
    6.34
    >>> projectile_sim(5, 0.5, 25, 0.785)
    0.0
    7.61
    12.77
    15.47
    15.72
    13.52
    8.87
    1.76
    >>> projectile_sim(10, 1, 50.0, 0.79)
    0.0
    30.61
    51.42
    62.41
    63.59
    54.96
    36.53
    8.28
    """
    for time in range(0, int(simulation_time / interval) + 1):
        time = time * interval 
        height = (-0.5 * GRAVITY_CONSTANT * (time**2)) +\
                     (velocity_i * math.sin(angle) * time)
        if height >= 0:
            print(round(height, 2))
        else:
            return None


def rocket_main():
    """
    The main function that runs the rocket simulation,
    interacting with the user to gather input and calculate various
    aspects of the rocket's trip, cost, loading, and trajectory simulation.
    
    Args:
        None
    
    Returns:
        None: Interacts with the user through input prompts
        and prints the simulation results.
    
    Examples:
    >>> rocket_main()
    Welcome to the Rocket Simulation!
    Enter the rocket radius in feet: 5
    Enter the rocket cone height in feet: 10
    Enter the rocket cylinder height in feet: 15
    Enter the exhaust velocity for the upcoming trip: 2500
    Enter the initial velocity for the upcoming trip: 3000
    Enter the angle of launch for the upcoming trip: 0.785
    Enter the length of the upcoming trip: 120
    Would you like to factor in tax? 1 for yes, 0 for no: 1
    This trip will cost $2202761.62
    Now loading the rocket:
    Please enter the weight of the next item
    (type "Done" when you are done filling the rocket): 100
    Enter item width: 5
    Enter item length: 5
    Enter item height: 5
    Please enter the weight of the next item
    (type "Done" when you are done filling the rocket): Done
    The rocket and its equipment will weigh 62342.78kg
    Enter the simulation total time: 10
    Enter the simulation interval: 2
    Now simulating the rocket trajectory:
    0.0
    4221.33
    8403.42
    12546.27
    16649.88
    20714.26
    """
    print("Welcome to the Rocket Simulation!")
    radius = feet_to_meter(float(input("Enter the rocket radius in feet: ")))
    height_cone = feet_to_meter(\
        float(input("Enter the rocket cone height in feet: ")))
    height_cyl = feet_to_meter(\
        float(input("Enter the rocket cylinder height in feet: ")))
    velocity_e = float(input\
                       ("Enter the exhaust velocity for the upcoming trip: "))
    velocity_i = float(input\
                       ("Enter the initial velocity for the upcoming trip: "))
    angle = float(input("Enter the angle of launch for the upcoming trip: "))
    flight_time = float(input("Enter the length of the upcoming trip: "))
    tax = int(input("Would you like to factor in tax? 1 for yes, 0 for no: "))
    print("This trip will cost $" +\
          str(calculate_cost(radius, height_cone, height_cyl, velocity_e,\
                   velocity_i, flight_time, tax)))
    print("Now loading the rocket:")
    rocket_initial_weight = rocket_mass(radius, height_cone, height_cyl)
    print("The rocket and its equipment will weigh " +\
          str(load_rocket(rocket_initial_weight, radius, height_cyl)) + "kg")
    simulation_time = float(input("Enter the simulation total time: "))
    interval = float(input("Enter the simulation interval: "))
    print("Now simulating the rocket trajectory:")
    projectile_sim(simulation_time, interval, velocity_i, angle)
    
