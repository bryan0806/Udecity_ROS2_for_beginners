from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld=LaunchDescription()

    robot_names = ["Giskard" , "BB8" , "Daneel", "Jander", "C3P0"]

    robot_news_stations_nodes = []

    for name in robot_names:
        robot_news_stations_nodes.append(Node(
        package="my_cpp_pkg2",
        executable="robot_news_station",
        name="robot_news_station_" + name.lower(),
        parameters=[
            {"robot_name" : name}
        ]
        )
        )

    smartphone = Node(
        package="my_cpp_pkg2",
        executable="smartphone",
        name="smartphone"
        )
    

    for node in robot_news_stations_nodes:
        ld.add_action(node)
    ld.add_action(smartphone)

    return ld